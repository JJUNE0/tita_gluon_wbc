"""VALIDATION_SIM: TITA model state and MuJoCo stepping; no policy conventions."""

from pathlib import Path
from collections import deque
import threading
import numpy as np

from .adapter import NATIVE_JOINTS

REPO = Path(__file__).resolve().parents[3]


class TitaMujocoEnv:
    def __init__(self, cfg, viewer_enabled=False):
        import mujoco
        self.mujoco, self.cfg = mujoco, cfg
        scene = Path(cfg['model']['scene_xml'])
        scene = scene if scene.is_absolute() else REPO / scene
        if cfg.get('learned_residual'):
            spec = mujoco.MjSpec.from_file(str(scene))
            for index, body in enumerate(list(spec.bodies)):
                if not body.name or body.name == 'world':
                    continue
                child = body.add_body(name=f'residual_payload_{index}')
                child.add_geom(name=f'residual_payload_icon_{index}', type=mujoco.mjtGeom.mjGEOM_BOX,
                               size=[.035, .035, .035], mass=1e-6, contype=0, conaffinity=0,
                               rgba=[1., .4, .06, 0.])
            self.model = spec.compile()
            for body in range(self.model.nbody):
                if self.model.body(body).name.startswith('residual_payload_'):
                    self.model.body_mass[body] = 0.
                    self.model.body_inertia[body] = 0.
        else:
            self.model = mujoco.MjModel.from_xml_path(str(scene))
        self.ground = (self.model.geom_bodyid == 0) & ((self.model.geom_contype != 0) | (self.model.geom_conaffinity != 0))
        friction = cfg['model'].get('ground_friction')
        if friction is not None:
            self.set_ground_friction(friction)
        if cfg['model'].get('flat_ground'):
            floor = self.model.geom('floor').id
            obstacles = (self.model.geom_bodyid == 0) & (np.arange(self.model.ngeom) != floor)
            self.model.geom_contype[obstacles] = self.model.geom_conaffinity[obstacles] = 0
            self.model.geom_rgba[obstacles, 3] = 0.
        if cfg['model'].get('wheel_collision') == 'sphere':
            for side in ('left', 'right'):
                body = self.model.body(f'{side}_leg_4').id
                geoms = [g for g in range(self.model.ngeom) if self.model.geom_bodyid[g] == body
                         and (self.model.geom_contype[g] or self.model.geom_conaffinity[g])]
                if len(geoms) != 1:
                    raise ValueError(f'Expected one wheel collision for {side}')
                geom = geoms[0]
                if self.model.geom_type[geom] not in (mujoco.mjtGeom.mjGEOM_CYLINDER, mujoco.mjtGeom.mjGEOM_SPHERE):
                    raise ValueError(f'Unsupported wheel collision for {side}')
                radius = float(self.model.geom_size[geom, 0])
                self.model.geom_type[geom] = mujoco.mjtGeom.mjGEOM_SPHERE
                self.model.geom_size[geom] = [radius, 0., 0.]
                self.model.geom_rbound[geom] = radius
                self.model.geom_aabb[geom] = [0., 0., 0., radius, radius, radius]
        self.data = mujoco.MjData(self.model)
        self.model.opt.timestep = float(cfg['control']['sim_timestep'])
        self.decimation = int(cfg['control']['decimation'])
        self.control_dt = self.model.opt.timestep * self.decimation
        self.joint_names = NATIVE_JOINTS
        joint_ids = [mujoco.mj_name2id(self.model, mujoco.mjtObj.mjOBJ_JOINT, name) for name in self.joint_names]
        self.actuator_ids = [mujoco.mj_name2id(self.model, mujoco.mjtObj.mjOBJ_ACTUATOR,
                                             name.removeprefix('joint_')) for name in self.joint_names]
        if min(joint_ids + self.actuator_ids) < 0:
            raise ValueError('The MuJoCo scene does not contain the configured TITA joints/actuators')
        self.qpos_addr = np.asarray([self.model.jnt_qposadr[index] for index in joint_ids])
        self.qvel_addr = np.asarray([self.model.jnt_dofadr[index] for index in joint_ids])
        self.sensor_rng = np.random.default_rng(42)
        self.delay_rng = np.random.default_rng(43)
        self.sensor_noise = dict(joint_position=0., joint_velocity=0., gyro=0., orientation_deg=0.)
        self.noise_time = None
        self.delay_steps = (0, 0)
        self.last_delay_ms = 0.
        self.torque_history = deque(maxlen=1)
        self.viewer, self._viewer_threads = None, []
        self.reset()
        if viewer_enabled:
            import mujoco.viewer
            self.viewer = mujoco.viewer.launch_passive(self.model, self.data, show_left_ui=False, show_right_ui=False)
            if cfg.get('gait_command'):
                self.viewer.cam.type = mujoco.mjtCamera.mjCAMERA_TRACKING
                self.viewer.cam.trackbodyid = self.model.body('base_link').id
                self.viewer.cam.distance = 1.5
                self.viewer.cam.elevation = -20.
            self._viewer_threads = [thread for thread in threading.enumerate()
                                    if getattr(getattr(thread, '_target', None), '__module__', None) == 'mujoco.viewer']

    def reset(self, joint_angles=None):
        self.mujoco.mj_resetData(self.model, self.data)
        robot = self.cfg['robot']
        self.data.qpos[:3] = robot['reset_base_pos']
        self.data.qpos[3:7] = robot['reset_base_quat']
        self.data.qpos[self.qpos_addr] = robot['default_joint_angles'] if joint_angles is None else joint_angles
        self.noise_time = None
        self._reset_delay()
        self.mujoco.mj_forward(self.model, self.data)

    def set_ground_friction(self, value):
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not np.isfinite(value) or value < 0:
            raise ValueError('model.ground_friction must be finite and non-negative')
        # Keep a stable priority when the slider is moved repeatedly.
        priority = int(np.max(self.model.geom_priority[~self.ground], initial=0)) + 1
        self.model.geom_priority[self.ground] = priority
        self.model.geom_friction[self.ground, 0] = value
        self.model.geom_condim[self.ground] = np.maximum(self.model.geom_condim[self.ground], 3)
        self.cfg['model']['ground_friction'] = float(value)

    def set_sensor_noise(self, joint_position=0., joint_velocity=0., gyro=0., orientation_deg=0.):
        values = dict(joint_position=joint_position, joint_velocity=joint_velocity,
                      gyro=gyro, orientation_deg=orientation_deg)
        if any(not np.isfinite(x) or x < 0 for x in values.values()):
            raise ValueError('Sensor standard deviations must be finite and non-negative')
        self.sensor_noise = {key: float(value) for key, value in values.items()}
        self.noise_time = None

    def _sensor_offsets(self):
        # All consumers share the same noisy sensor sample at one physics time.
        if self.noise_time != self.data.time:
            self.noise_offsets = {}
            for key, size in (('joint_position', 8), ('joint_velocity', 8), ('gyro', 3), ('orientation_deg', 3)):
                sigma = self.sensor_noise[key]
                if key == 'orientation_deg':
                    sigma = np.radians(sigma)
                self.noise_offsets[key] = self.sensor_rng.normal(0., sigma, size) if sigma else np.zeros(size)
            self.noise_time = float(self.data.time)
        return self.noise_offsets

    def set_torque_delay(self, minimum_ms, maximum_ms):
        if (not np.isfinite([minimum_ms, maximum_ms]).all()
                or not 0 <= minimum_ms <= maximum_ms <= 100):
            raise ValueError('Torque delay requires 0 <= minimum <= maximum <= 100 ms')
        tick_ms = self.model.opt.timestep * 1000.
        self.delay_steps = tuple(int(np.ceil(value / tick_ms - 1e-9)) for value in (minimum_ms, maximum_ms))
        self._reset_delay()

    def _reset_delay(self):
        # Start a changed delay with the currently applied command, without a
        # synthetic zero-torque impulse. Reset physics starts with zero ctrl.
        maximum = self.delay_steps[1]
        held = self.data.ctrl[self.actuator_ids].copy()
        self.torque_history = deque((held.copy() for _ in range(maximum)), maxlen=maximum+1)
        self.last_delay_ms = 0.

    def delayed_torque(self, torque):
        low, high = self.delay_steps
        if high == 0:
            return torque
        self.torque_history.append(np.asarray(torque).copy())
        lag = low if low == high else int(self.delay_rng.integers(low, high+1))
        self.last_delay_ms = lag * self.model.opt.timestep * 1000.
        return self.torque_history[-1-lag].copy()

    def perturbation_settings(self):
        return dict(ground_friction=self.cfg['model'].get('ground_friction'),
                    sensor_noise_std=self.sensor_noise.copy(), sensor_seed=42, delay_seed=43,
                    torque_delay_range_ms=[step*self.model.opt.timestep*1000. for step in self.delay_steps],
                    last_torque_delay_ms=self.last_delay_ms,
                    delay_model='Common eight-joint command-history lag, uniformly resampled each physics tick')

    def joint_pos(self):
        value = self.data.qpos[self.qpos_addr].copy()
        if self.sensor_noise['joint_position']:
            value += self._sensor_offsets()['joint_position']
        return value.astype(np.float32)

    def joint_vel(self):
        value = self.data.qvel[self.qvel_addr].copy()
        if self.sensor_noise['joint_velocity']:
            value += self._sensor_offsets()['joint_velocity']
        return value.astype(np.float32)

    def base_pos(self):
        return self.data.qpos[:3].astype(np.float32).copy()

    def base_quat(self):
        return self.data.qpos[3:7].astype(np.float32).copy()

    def base_lin_vel(self):
        return self.data.qvel[:3].astype(np.float32).copy()

    def base_quat_sensor(self):
        value = self.data.sensor('trunk_quat').data.copy()
        if self.sensor_noise['orientation_deg']:
            rotation = self._sensor_offsets()['orientation_deg']
            angle = np.linalg.norm(rotation)
            delta = np.r_[np.cos(angle/2), rotation*np.sinc(angle/(2*np.pi))*.5]
            product = np.empty(4)
            self.mujoco.mju_mulQuat(product, value, delta)
            value = product / np.linalg.norm(product)
        return value.astype(np.float32)

    def base_ang_vel(self):
        value = self.data.sensor('trunk_gyro').data.copy()
        if self.sensor_noise['gyro']:
            value += self._sensor_offsets()['gyro']
        return value.astype(np.float32)

    def step_with_torque_callback(self, callback):
        for _ in range(self.decimation):
            torque = callback(self.joint_pos(), self.joint_vel())
            if not np.isfinite(torque).all():
                raise ValueError('Non-finite torque')
            self.data.ctrl[self.actuator_ids] = self.delayed_torque(torque)
            self.mujoco.mj_step(self.model, self.data)
        if self.cfg.get('learned_residual'):
            self.mujoco.mj_forward(self.model, self.data)
        if self.viewer is not None:
            self.viewer.sync()

    def is_running(self):
        return self.viewer is None or self.viewer.is_running()

    def close(self):
        if self.viewer is not None:
            self.viewer.close()
            for thread in self._viewer_threads:
                thread.join(timeout=5.)
            self.viewer = None
