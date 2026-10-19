"""VALIDATION_SIM: URDF rigid-body composition and motor-reaction WIP model."""

import xml.etree.ElementTree as ET
import numpy as np
from scipy.linalg import expm, solve_discrete_are
from scipy.spatial.transform import Rotation

from sim2sim_ros2_jazzy.adapter import NATIVE_JOINTS


def vector(element, key, default='0 0 0'):
    return np.fromstring(element.get(key, default), sep=' ')


class Description:
    def __init__(self, urdf):
        self.root = ET.parse(urdf).getroot()
        self.links = {link.get('name'): link for link in self.root.findall('link')}
        self.joints = list(self.root.findall('joint'))
        self.children = {joint.find('child').get('link'): joint for joint in self.joints}
        self.wheel_links = [self.root.find(f"joint[@name='{NATIVE_JOINTS[i]}']/child").get('link')
                            for i in (3, 7)]
        radii = [float(self.links[name].find('collision/geometry/cylinder').get('radius'))
                 for name in self.wheel_links]
        if not np.allclose(radii, radii[0]):
            raise ValueError('Unequal wheel radii require a different estimator')
        self.radius = radii[0]

    def frames(self, q):
        positions = dict(zip(NATIVE_JOINTS, q))
        frames = {'base_link': np.eye(4)}
        axes = {}
        pending = self.joints.copy()
        while pending:
            progressed = False
            for joint in pending.copy():
                parent = joint.find('parent').get('link')
                if parent not in frames:
                    continue
                origin = joint.find('origin')
                local = np.eye(4)
                local[:3, :3] = Rotation.from_euler('xyz', vector(origin, 'rpy')).as_matrix()
                local[:3, 3] = vector(origin, 'xyz')
                frame = frames[parent] @ local
                name = joint.get('name')
                if joint.get('type') != 'fixed':
                    axis = vector(joint.find('axis'), 'xyz')
                    axes[name] = frame[:3, :3] @ axis
                    frame[:3, :3] = frame[:3, :3] @ Rotation.from_rotvec(axis * positions[name]).as_matrix()
                frames[joint.find('child').get('link')] = frame
                pending.remove(joint)
                progressed = True
            if not progressed:
                raise ValueError('Unresolved URDF kinematic tree')
        return frames, axes

    def wheel_chains(self):
        chains = []
        for link in self.wheel_links:
            chain = []
            while link in self.children:
                joint = self.children[link]
                if joint.get('name') in NATIVE_JOINTS:
                    chain.append(NATIVE_JOINTS.index(joint.get('name')))
                link = joint.find('parent').get('link')
            chains.append(chain)
        return chains

    def nominal(self, q, gravity=9.81):
        frames, axes = self.frames(q)
        bodies, wheels = [], []
        for name, link in self.links.items():
            inertial = link.find('inertial')
            if inertial is None:
                continue
            mass = float(inertial.find('mass').get('value'))
            origin = inertial.find('origin')
            rotation = frames[name][:3, :3] @ Rotation.from_euler('xyz', vector(origin, 'rpy')).as_matrix()
            com = frames[name][:3, :3] @ vector(origin, 'xyz') + frames[name][:3, 3]
            tensor = inertial.find('inertia')
            inertia = np.array([[float(tensor.get('i' + ''.join(sorted(a + b))))
                                 for b in 'xyz'] for a in 'xyz'])
            inertia = rotation @ inertia @ rotation.T
            entry = (mass, com, inertia)
            (wheels if name in self.wheel_links else bodies).append(entry)
        mass = sum(item[0] for item in bodies)
        com = sum(m * p for m, p, _ in bodies) / mass
        axle = np.mean([frames[name][:3, 3] for name in self.wheel_links], axis=0)
        axle_delta = frames[self.wheel_links[0]][:3, 3] - frames[self.wheel_links[1]][:3, 3]
        equilibrium_roll = float(-np.arctan2(axle_delta[2], axle_delta[1]))
        level_rotation = Rotation.from_euler('x', equilibrium_roll).as_matrix()
        offset = com - axle
        offset = level_rotation @ offset
        length = float(np.linalg.norm(offset[[0, 2]]))
        pitch_inertia = sum(I[1, 1] + m * np.sum((p - com)[[0, 2]]**2) for m, p, I in bodies)
        wheel_mass = np.mean([item[0] for item in wheels])
        wheel_inertia = np.mean([axes[NATIVE_JOINTS[index]] @ item[2] @ axes[NATIVE_JOINTS[index]]
                                 for index, item in zip((3, 7), wheels)])
        return dict(m_b=mass, m_w=float(wheel_mass), I_w=float(wheel_inertia),
                    I_b=float(pitch_inertia), l=length, r=self.radius, g=gravity,
                    equilibrium_pitch=float(-np.arctan2(offset[0], offset[2])),
                    equilibrium_roll=equilibrium_roll,
                    com_base=com.tolist(), axle_base=axle.tolist())


def continuous(parameters):
    mb, mw, iw, ib, l, r, g = [parameters[k] for k in ('m_b', 'm_w', 'I_w', 'I_b', 'l', 'r', 'g')]
    if not np.isfinite([mb, mw, iw, ib, l, r, g]).all() or min(mb, mw, iw, ib, l, r, g) <= 0:
        raise ValueError('Invalid physical parameters')
    M, C, J, G = mb + 2*mw + 2*iw/r**2, mb*l, ib + mb*l*l, mb*g*l
    D = M*J - C*C
    if D <= 0:
        raise ValueError('Nonpositive mass-matrix determinant')
    A = np.zeros((4, 4))
    A[0, 1], A[2, 3] = 1., 1.
    A[1, 2], A[3, 2] = -C*G/D, M*G/D
    B = np.array([[0.], [(J/r+C)/D], [0.], [-(M+C/r)/D]])
    return A, B


def discrete(parameters, dt, dimension=4):
    if dt <= 0 or dimension not in (3, 4):
        raise ValueError('Invalid timestep or state dimension')
    A, B = continuous(parameters)
    block = np.zeros((5, 5))
    block[:4, :4], block[:4, 4:] = A, B
    zoh = expm(block * dt)
    indices = np.arange(4) if dimension == 4 else np.arange(1, 4)
    return zoh[np.ix_(indices, indices)], zoh[indices, 4:]


def residual_matrices(coefficients, dt, dimension=4):
    av, bv, aw, bw = np.asarray(coefficients).reshape(4)
    A = np.zeros((4, 4))
    A[:, 2] = [dt*av/2, av, dt*aw/2, aw]
    B = np.array([[dt*bv/2], [bv], [dt*bw/2], [bw]])
    return (A, B) if dimension == 4 else (A[1:, 1:], B[1:])


def dlqr(A, B, Q, R, margin=1e-7):
    n = len(A)
    controllability = np.column_stack([np.linalg.matrix_power(A, i) @ B for i in range(n)])
    if not np.isfinite(A).all() or not np.isfinite(B).all():
        raise ValueError('Non-finite candidate model')
    if np.linalg.matrix_rank(controllability) != n:
        raise ValueError('Uncontrollable candidate model')
    if not np.allclose(Q, Q.T) or np.linalg.eigvalsh(Q).min() < 0 or R <= 0:
        raise ValueError('Invalid Q/R')
    P = solve_discrete_are(A, B, Q, np.array([[R]]))
    K = np.linalg.solve(np.array([[R]]) + B.T @ P @ B, B.T @ P @ A)
    eigenvalues = np.linalg.eigvals(A - B @ K)
    if not np.isfinite(K).all() or max(abs(eigenvalues)) >= 1 - margin:
        raise ValueError('Unstable candidate gain')
    return K.reshape(n), eigenvalues
