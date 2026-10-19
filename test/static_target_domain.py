"""VALIDATION_SIM: fixed target physics before the very first startup mj_step."""
import copy
import hashlib
from unittest.mock import patch

import numpy as np

from flash_overnight_model_stages import Runner, KEYS, CKPT, REPO, prepared_config, current
from sim2sim_ros2_jazzy.mujoco_env import TitaMujocoEnv


class StartupFailure(RuntimeError):
    pass


class StaticEnv(TitaMujocoEnv):
    def __init__(self, cfg, target):
        super().__init__(cfg)
        self.target = copy.deepcopy(target)
        self.motor_state = np.zeros(2)
        self.physical = []
        self.startup = []
        self.record_startup = True
        m, mj = self.model, self.mujoco
        before = self.data.qpos.copy(), self.data.qvel.copy()
        factor = target.get('mass', 1.)
        m.body_mass[1:] *= factor
        m.body_inertia[1:] *= factor
        base = m.body('base_link').id
        m.body_ipos[base, 0] += target.get('com', 0.)
        floor = m.geom('floor').id
        wheel_bodies = [int(m.jnt_bodyid[m.joint(self.joint_names[i]).id]) for i in [3, 7]]
        wheel_geoms = [i for i in range(m.ngeom) if m.geom_bodyid[i] in wheel_bodies]
        if 'friction' in target:
            m.geom_friction[[floor]+wheel_geoms, 0] = target['friction']
        assert np.all(m.body_inertia[1:] > 0.)
        inertia = np.sort(m.body_inertia[1:], axis=1)
        assert np.all(inertia[:, 2] <= inertia[:, :2].sum(1)+1e-12)
        mj.mj_setConst(m, mj.MjData(m))
        mj.mj_forward(m, self.data)
        np.testing.assert_array_equal(before[0], self.data.qpos)
        np.testing.assert_array_equal(before[1], self.data.qvel)
        self.initial_fingerprint = self.fingerprint()
        self.metadata = dict(target=copy.deepcopy(target), configured_before_first_step=True,
            com_body='base_link', com_offset_m=target.get('com', 0.),
            com_tensor='positive principal inertia about translated CoM; orientation and tensor preserved',
            mass_inertia_factor=factor, floor_friction=float(m.geom_friction[floor, 0]),
            wheel_friction=m.geom_friction[wheel_geoms, 0].tolist(),
            fingerprint=self.initial_fingerprint, startup_steps=0)

    def fingerprint(self):
        values = [self.model.body_mass, self.model.body_inertia, self.model.body_ipos,
                  self.model.geom_friction, np.array([self.target.get('gain', 1.), self.target.get('lag', 0.),
                  self.model.opt.timestep])]
        return hashlib.sha256(b''.join(np.asarray(v).tobytes() for v in values)).hexdigest()

    def assert_static(self):
        assert self.fingerprint() == self.initial_fingerprint

    def step_with_torque_callback(self, callback):
        self.physical = []
        for _ in range(self.decimation):
            command = np.asarray(callback(self.joint_pos(), self.joint_vel())).copy()
            value = command.copy()
            desired = command[[3, 7]]*self.target.get('gain', 1.)
            lag = self.target.get('lag', 0.)
            self.motor_state = (self.motor_state+(1.-np.exp(-self.model.opt.timestep/lag))*(desired-self.motor_state)
                                if lag else desired.copy())
            value[[3, 7]] = np.clip(self.motor_state, -12., 12.)
            np.testing.assert_array_equal(value[[0, 1, 2, 4, 5, 6]], command[[0, 1, 2, 4, 5, 6]])
            assert np.isfinite(value).all()
            self.data.ctrl[self.actuator_ids] = value
            self.physical.append(value.copy())
            self.mujoco.mj_step(self.model, self.data)
        if self.record_startup:
            self.startup.append(dict(qpos=self.data.qpos.copy(), qvel=self.data.qvel.copy(),
                                     motor=np.asarray(self.physical)))
            self.metadata['startup_steps'] += 1
            q = self.data.qpos[3:7]
            # Quaternion tilt guard allows the intended crouched stand transition.
            up_z = 1.-2.*(q[1]**2+q[2]**2)
            if not np.isfinite(np.r_[self.data.qpos, self.data.qvel]).all() or up_z < np.cos(.9) or self.data.qpos[2] < .025:
                exc=StartupFailure(f'startup_finite_tilt_or_height z={self.data.qpos[2]} up_z={up_z}')
                exc.env=self
                raise exc


class StaticRunner(Runner):
    def __init__(self, cfg, job, target):
        created = []
        def factory(config):
            env = StaticEnv(config, target)
            created.append(env)
            return env
        self.created = created
        with patch('sim2sim.lqr.runtime.TitaMujocoEnv', factory):
            super().__init__(cfg, job)
        self.env.record_startup = False
        self.env.assert_static()

    def step(self, residual):
        result = super().step(residual)
        result['physical_motor'] = np.asarray(self.env.physical)
        return result

    def full_snapshot(self):
        return self.snapshot(), self.env.motor_state.copy()

    def full_restore(self, snapshot):
        self.restore(snapshot[0])
        self.env.motor_state = snapshot[1].copy()
        self.env.assert_static()

    def contact_metadata(self):
        m, mj = self.env.model, self.env.mujoco
        d = mj.MjData(m)
        mj.mj_copyData(d, m, self.env.data)
        mj.mj_forward(m, d)
        floor = m.geom('floor').id
        return [dict(geoms=c.geom.tolist(), dim=int(c.dim), friction=float(c.friction[0]))
                for c in d.contact[:d.ncon] if floor in c.geom]


def sensor_state(r, p_hold):
    z = current(r)[[0, 1, 2, 3]+list(range(5, 25))].copy()
    z[0] -= p_hold
    return z
