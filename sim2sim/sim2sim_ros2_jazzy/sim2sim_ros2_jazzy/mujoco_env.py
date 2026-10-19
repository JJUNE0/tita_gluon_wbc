"""VALIDATION_SIM: TITA model state and MuJoCo stepping; no policy conventions."""

from pathlib import Path
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
        self.model = mujoco.MjModel.from_xml_path(str(scene))
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
        self.viewer, self._viewer_threads = None, []
        self.reset()
        if viewer_enabled:
            import mujoco.viewer
            self.viewer = mujoco.viewer.launch_passive(self.model, self.data, show_left_ui=False, show_right_ui=False)
            self._viewer_threads = [thread for thread in threading.enumerate()
                                    if getattr(getattr(thread, '_target', None), '__module__', None) == 'mujoco.viewer']

    def reset(self, joint_angles=None):
        self.mujoco.mj_resetData(self.model, self.data)
        robot = self.cfg['robot']
        self.data.qpos[:3] = robot['reset_base_pos']
        self.data.qpos[3:7] = robot['reset_base_quat']
        self.data.qpos[self.qpos_addr] = robot['default_joint_angles'] if joint_angles is None else joint_angles
        self.mujoco.mj_forward(self.model, self.data)

    def joint_pos(self):
        return self.data.qpos[self.qpos_addr].astype(np.float32).copy()

    def joint_vel(self):
        return self.data.qvel[self.qvel_addr].astype(np.float32).copy()

    def base_pos(self):
        return self.data.qpos[:3].astype(np.float32).copy()

    def base_quat(self):
        return self.data.qpos[3:7].astype(np.float32).copy()

    def base_lin_vel(self):
        return self.data.qvel[:3].astype(np.float32).copy()

    def base_quat_sensor(self):
        return self.data.sensor('trunk_quat').data.astype(np.float32).copy()

    def base_ang_vel(self):
        return self.data.sensor('trunk_gyro').data.astype(np.float32).copy()

    def step_with_torque_callback(self, callback):
        for _ in range(self.decimation):
            torque = callback(self.joint_pos(), self.joint_vel())
            if not np.isfinite(torque).all():
                raise ValueError('Non-finite torque')
            self.data.ctrl[self.actuator_ids] = torque
            self.mujoco.mj_step(self.model, self.data)
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
