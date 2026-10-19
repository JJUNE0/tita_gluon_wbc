"""VALIDATION_SIM: reuse the launch policy, observation, PD and physics path."""

import json
import numpy as np
import onnxruntime as ort

from . import REPO
from sim2sim_ros2_jazzy.adapter import ActionAdapter, ObservationBuilder, ObsState, quat_wxyz_to_rotmat
from sim2sim_ros2_jazzy.checkpoint import prepared_config
from sim2sim_ros2_jazzy.mujoco_env import TitaMujocoEnv

CHECKPOINT = REPO / 'lab/ddt_lab/logs/flash_sac/tita_flash_sac_172127_928297/model_100000'
WHEELS = np.array([3, 7])
LEGS = np.array([0, 1, 2, 4, 5, 6])


def policy_config():
    path = prepared_config(CHECKPOINT)
    if path is None:
        raise RuntimeError('BLOCKED: run the existing launch --prepare-only for model_100000 first')
    cfg = json.loads(path.read_text())
    if cfg['policy_interface']['algorithm'] != 'FlashSAC':
        raise ValueError('This ablation requires the designated FlashSAC actor')
    return cfg


class Playback:
    def __init__(self, cfg):
        self.cfg = cfg
        self.env = TitaMujocoEnv(cfg)
        self.builder = ObservationBuilder(cfg)
        self.adapter = ActionAdapter(cfg)
        options = ort.SessionOptions()
        options.intra_op_num_threads = 1
        self.policy = ort.InferenceSession(cfg['policy']['path'], sess_options=options,
                                           providers=['CPUExecutionProvider'])
        self.last_action = np.zeros(8, dtype=np.float32)

    def infer(self, command=None):
        env = self.env
        quaternion = env.base_quat_sensor()
        command = np.zeros(3, dtype=np.float32) if command is None else command
        state = ObsState(env.joint_pos(), env.joint_vel(), quaternion, env.base_ang_vel(),
                         command, self.last_action,
                         quat_wxyz_to_rotmat(quaternion).T @ env.base_lin_vel())
        obs = self.builder.build(state)
        action = self.policy.run(['nn_output'], {'nn_input0': obs.reshape(1, -1)})[0].reshape(8)
        return obs, action

    def step(self, action, override=None, motor=None):
        commands, torques = [], []

        def callback(q, dq):
            torque = self.adapter.compute(action, q, dq)
            if override is not None:
                torque = override(q, dq, torque)
            torque = np.clip(torque, -self.adapter.limit, self.adapter.limit)
            commands.append(torque.copy())
            if motor is not None:
                torque = motor(torque)
            torques.append(torque.copy())
            return torque

        self.env.step_with_torque_callback(callback)
        self.last_action = action.copy()
        return np.asarray(commands), np.asarray(torques)
