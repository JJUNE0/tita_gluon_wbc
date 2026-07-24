"""Gym registration for standalone GLUON reach tasks."""

import gymnasium as gym

from . import joint_pos_env_cfg


gym.register(
    id="DDT-Reach-Gluon-2L6-4L3-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    disable_env_checker=True,
    kwargs={"env_cfg_entry_point": joint_pos_env_cfg.GluonReachEnvCfg},
)

gym.register(
    id="DDT-Reach-Gluon-2L6-4L3-Play-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    disable_env_checker=True,
    kwargs={"env_cfg_entry_point": joint_pos_env_cfg.GluonReachEnvCfg_PLAY},
)

