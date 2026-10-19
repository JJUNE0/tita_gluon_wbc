"""VALIDATION_SIM: command-gated encoder/IMU hold added to policy wheel torque."""

import numpy as np
from scipy.spatial.transform import Rotation


class ResidualWheelPD:
    def __init__(self, env):
        self.env = env
        self.data = env.mujoco.MjData(env.model)
        self.joints = np.array([env.model.joint(name).id for name in env.joint_names])
        radii = [env.model.geom_size[next(g for g in range(env.model.ngeom)
                 if env.model.geom_bodyid[g] == env.model.jnt_bodyid[j]
                 and env.model.geom_type[g] == env.mujoco.mjtGeom.mjGEOM_CYLINDER), 0]
                 for j in self.joints[[3, 7]]]
        if min(radii) <= 0 or not np.allclose(radii, radii[0]):
            raise ValueError('Residual hold requires equal positive wheel radii')
        self.radius = float(radii[0])
        self.limit = np.asarray(env.cfg['robot']['torque_limit'])[[3, 7]]
        self.reset()

    def reset(self):
        self.holding = False
        self.position = self.velocity = self.age = self.u = 0.
        self.previous = None

    @property
    def slew_rate(self):
        return 2.  # Total residual torque, Nm/s.

    def update(self, command):
        if command is None:  # Reset on leaving RL, including operator reset.
            self.reset()
            return
        env, dt = self.env, self.env.control_dt
        # Refresh a clone only: actor and hold share current IMU without changing physics.
        env.mujoco.mj_copyData(self.data, env.model, env.data)
        env.mujoco.mj_forward(env.model, self.data)
        rotation = Rotation.from_quat(self.data.sensor('trunk_quat').data[[1, 2, 3, 0]])
        yaw = rotation.as_euler('xyz')[2]
        lateral = np.array([-np.sin(yaw), np.cos(yaw), 0.])
        projections = self.data.xaxis[self.joints] @ lateral
        self.signs = np.sign(projections[[3, 7]])
        if not self.holding and np.all(abs(command) <= np.array([.02, .02, .03])):
            self.holding = True
            self.position = self.age = 0.
            self.previous = None
        elif self.holding and np.any(abs(command) >= np.array([.04, .04, .06])):
            self.holding = False
        target = 0.
        if self.holding:
            q, dq = env.joint_pos(), env.joint_vel()
            body_rate = lateral @ rotation.apply(self.data.sensor('trunk_gyro').data)
            self.velocity = self.radius * np.mean(body_rate + (projections * dq).reshape(2, 4).sum(1))
            if self.previous is not None:
                prev_q, prev_rotation, prev_projections = self.previous
                delta_body = lateral @ (rotation * prev_rotation.inv()).as_rotvec()
                delta = ((projections + prev_projections) / 2 * (q - prev_q)).reshape(2, 4).sum(1)
                self.position += self.radius * np.mean(delta_body + delta)
            self.previous = (q.copy(), rotation, projections)
            target = self._target(rotation)
            self.age += dt
        delta = self.slew_rate * dt
        self.u = float(np.clip(target, self.u - delta, self.u + delta))

    def _target(self, rotation):
        phase = min(self.age / 1.5, 1.)
        ramp = phase * phase * (3. - 2. * phase)
        return ramp * np.clip(-2. * self.position - 24. * self.velocity, -2., 2.)

    def apply(self, torque):
        torque = torque.copy()
        torque[[3, 7]] = np.clip(torque[[3, 7]] + self.u * self.signs / 2, -self.limit, self.limit)
        return torque
