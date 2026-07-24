from __future__ import annotations

import time
from typing import Any

import numpy as np


class TitaMujocoEnv:
    def __init__(self, cfg: dict[str, Any], viewer_enabled: bool | None = None):
        try:
            import mujoco
        except ImportError as exc:
            raise RuntimeError("mujoco is required. Install it with: python3 -m pip install mujoco") from exc

        self.mujoco = mujoco
        self.cfg = cfg
        self.model = mujoco.MjModel.from_xml_path(cfg["model"]["scene_xml"])
        self.data = mujoco.MjData(self.model)
        self.model.opt.timestep = float(cfg["control"]["sim_timestep"])
        self.decimation = int(cfg["control"].get("decimation", 1))
        self.real_time = bool(cfg["control"].get("real_time", True))
        self.control_dt = self.model.opt.timestep * self.decimation
        self._last_wall_time = time.monotonic()

        robot = cfg["robot"]
        self.joint_names = list(robot["joint_names"])
        self.actuator_names = list(robot["actuator_names"])
        self.base_body_name = robot["base_body_name"]
        self.imu_quat_sensor = robot["imu_quat_sensor"]
        self.imu_gyro_sensor = robot["imu_gyro_sensor"]
        self.imu_accel_sensor = robot["imu_accel_sensor"]

        self.joint_ids = [mujoco.mj_name2id(self.model, mujoco.mjtObj.mjOBJ_JOINT, n) for n in self.joint_names]
        self.actuator_ids = [
            mujoco.mj_name2id(self.model, mujoco.mjtObj.mjOBJ_ACTUATOR, n) for n in self.actuator_names
        ]
        if any(i < 0 for i in self.joint_ids):
            missing = [n for n, i in zip(self.joint_names, self.joint_ids) if i < 0]
            raise ValueError(f"Missing MuJoCo joints: {missing}")
        if any(i < 0 for i in self.actuator_ids):
            missing = [n for n, i in zip(self.actuator_names, self.actuator_ids) if i < 0]
            raise ValueError(f"Missing MuJoCo actuators: {missing}")

        self.qpos_addr = np.array([self.model.jnt_qposadr[i] for i in self.joint_ids], dtype=np.int32)
        self.qvel_addr = np.array([self.model.jnt_dofadr[i] for i in self.joint_ids], dtype=np.int32)
        self.viewer = None
        self.viewer_enabled = cfg["viewer"]["enabled"] if viewer_enabled is None else viewer_enabled
        self.reset()

        if self.viewer_enabled:
            self._launch_viewer()

    def _launch_viewer(self) -> None:
        try:
            import mujoco.viewer
        except Exception as exc:
            raise RuntimeError("MuJoCo passive viewer is unavailable in this environment") from exc
        self.viewer = mujoco.viewer.launch_passive(self.model, self.data)
        self.viewer.opt.flags[self.mujoco.mjtVisFlag.mjVIS_TRANSPARENT] = False
        if "show_left_ui" in self.cfg["viewer"]:
            self.viewer._hide_menus = not bool(self.cfg["viewer"].get("show_left_ui", False))

    def reset(self) -> None:
        self.mujoco.mj_resetData(self.model, self.data)
        robot = self.cfg["robot"]
        self.data.qpos[0:3] = np.asarray(robot["reset_base_pos"], dtype=np.float64)
        self.data.qpos[3:7] = np.asarray(robot["reset_base_quat"], dtype=np.float64)
        reset_joint_angles = robot.get("reset_joint_angles", robot["standing_joint_angles"])
        self.data.qpos[self.qpos_addr] = np.asarray(reset_joint_angles, dtype=np.float64)
        self.data.qvel[:] = 0.0
        self.data.ctrl[:] = 0.0
        self.mujoco.mj_forward(self.model, self.data)
        self._last_wall_time = time.monotonic()

    def reset_to_joint_angles(self, joint_angles: np.ndarray) -> None:
        self.reset()
        self.data.qpos[self.qpos_addr] = np.asarray(joint_angles, dtype=np.float64)
        self.data.qvel[:] = 0.0
        self.data.ctrl[:] = 0.0
        self.mujoco.mj_forward(self.model, self.data)
        self._last_wall_time = time.monotonic()

    def close(self) -> None:
        if self.viewer is not None:
            self.viewer.close()
            self.viewer = None

    def is_running(self) -> bool:
        return self.viewer is None or self.viewer.is_running()

    def joint_pos(self) -> np.ndarray:
        return self.data.qpos[self.qpos_addr].astype(np.float32).copy()

    def joint_vel(self) -> np.ndarray:
        return self.data.qvel[self.qvel_addr].astype(np.float32).copy()

    def base_quat(self) -> np.ndarray:
        # MuJoCo freejoint quaternion is [w, x, y, z].
        return self.data.qpos[3:7].astype(np.float32).copy()

    def base_pos(self) -> np.ndarray:
        return self.data.qpos[0:3].astype(np.float32).copy()

    def base_ang_vel(self) -> np.ndarray:
        try:
            return self.data.sensor(self.imu_gyro_sensor).data.astype(np.float32).copy()
        except KeyError:
            return self.data.qvel[3:6].astype(np.float32).copy()

    def base_lin_vel(self) -> np.ndarray:
        return self.data.qvel[0:3].astype(np.float32).copy()

    def body_quat(self, name: str) -> np.ndarray:
        """World-frame body orientation, [w, x, y, z]. Used for the wheel-vel
        base_lin_vel estimator (My18-style sim2sim) -- resolves the body id
        once and caches it."""
        cache = getattr(self, "_body_id_cache", None)
        if cache is None:
            cache = {}
            self._body_id_cache = cache
        body_id = cache.get(name)
        if body_id is None:
            body_id = self.mujoco.mj_name2id(self.model, self.mujoco.mjtObj.mjOBJ_BODY, name)
            if body_id < 0:
                raise ValueError(f"Missing MuJoCo body: {name!r}")
            cache[name] = body_id
        return self.data.xquat[body_id].astype(np.float32).copy()

    def base_accel(self) -> np.ndarray:
        try:
            return self.data.sensor(self.imu_accel_sensor).data.astype(np.float32).copy()
        except KeyError:
            return np.zeros(3, dtype=np.float32)

    def base_quat_sensor(self) -> np.ndarray:
        try:
            return self.data.sensor(self.imu_quat_sensor).data.astype(np.float32).copy()
        except KeyError:
            return self.base_quat()

    def set_torque(self, torque: np.ndarray) -> None:
        self.data.ctrl[self.actuator_ids] = np.asarray(torque, dtype=np.float64)

    def hold_standing_pd(self) -> np.ndarray:
        robot = self.cfg["robot"]
        target = np.asarray(robot["standing_joint_angles"], dtype=np.float32)
        return self.target_pd(target)

    def target_pd(self, target: np.ndarray, wheel_mode: str = "zero_velocity") -> np.ndarray:
        robot = self.cfg["robot"]
        q = self.joint_pos()
        dq = self.joint_vel()
        target = np.asarray(target, dtype=np.float32)
        kp = np.asarray(robot["joint_kp"], dtype=np.float32)
        kd = np.asarray(robot["joint_kd"], dtype=np.float32)
        limit = np.asarray(robot["torque_limit"], dtype=np.float32)
        torque = kp * (target - q) - kd * dq
        if wheel_mode == "zero_velocity":
            for idx in robot.get("wheel_indices", []):
                i = int(idx)
                torque[i] = -kd[i] * dq[i]
        torque = np.clip(torque, -limit, limit)
        return torque.astype(np.float32)

    def step(self) -> None:
        for _ in range(self.decimation):
            self.mujoco.mj_step(self.model, self.data)
        if self.viewer is not None:
            self.viewer.sync()
        if self.real_time:
            elapsed = time.monotonic() - self._last_wall_time
            sleep_time = self.control_dt - elapsed
            if sleep_time > 0.0:
                time.sleep(sleep_time)
            self._last_wall_time = time.monotonic()

    def step_with_torque_callback(self, callback, num_substeps: int | None = None, sleep: bool = True) -> None:
        """Step while recomputing torque every physics substep.

        The policy action target is held by the caller, but PD/velocity-servo torque
        should depend on the current q/qvel at each MuJoCo substep.
        """
        substeps = self.decimation if num_substeps is None else int(num_substeps)
        for _ in range(substeps):
            self.set_torque(callback(self.joint_pos(), self.joint_vel()))
            self.mujoco.mj_step(self.model, self.data)
        if self.viewer is not None:
            self.viewer.sync()
        if self.real_time and sleep:
            elapsed = time.monotonic() - self._last_wall_time
            expected_dt = self.model.opt.timestep * substeps
            sleep_time = expected_dt - elapsed
            if sleep_time > 0.0:
                time.sleep(sleep_time)
            self._last_wall_time = time.monotonic()

    def model_summary(self) -> str:
        lines = [
            f"nq={self.model.nq}",
            f"nv={self.model.nv}",
            f"nu={self.model.nu}",
            f"joints={self.joint_names}",
            f"actuators={self.actuator_names}",
            f"qpos_addr={self.qpos_addr.tolist()}",
            f"qvel_addr={self.qvel_addr.tolist()}",
        ]
        return "\n".join(lines)
