# Copyright (c) 2022-2025, The Isaac Lab Project Developers (https://github.com/isaac-sim/IsaacLab/blob/main/CONTRIBUTORS.md).
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

import sys

import gymnasium as gym

from . import agents, flat_env_cfg, jump_env_cfg, rough_env_cfg
from .real2sim import base_env_cfg

# Saved config.pkl files still resolve the deleted module's classes here.
sys.modules[f"{__name__}.my_flat_env_cfg"] = base_env_cfg



##
# Flat uses the selected 35-observation FlashSAC/PPO configuration.
# Historical My IDs retain their 33-observation baseline; jump/rough use NP3O.
##

gym.register(
    id="DDT-Velocity-Flat-Tita-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": flat_env_cfg.TitaFlatEnvCfg,
        "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:TitaFlatEstimatorPPORunnerCfg",
        "flash_sac_cfg_entry_point": f"{agents.__name__}.flash_sac_cfg:TitaFlatFlashSACRunnerCfg",
    },
)

gym.register(
    id="DDT-Velocity-Flat-Tita-Play-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": flat_env_cfg.TitaFlatEnvCfg_PLAY,
        "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:TitaFlatEstimatorPPORunnerCfg",
        "flash_sac_cfg_entry_point": f"{agents.__name__}.flash_sac_cfg:TitaFlatFlashSACRunnerCfg",
    },
)

gym.register(
    id="DDT-Velocity-Flat-Tita-My-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": base_env_cfg.MyTitaFlatEnvCfg,
        "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:TitaFlatEstimatorPPORunnerCfg",
        "flash_sac_cfg_entry_point": f"{agents.__name__}.flash_sac_cfg:TitaFlatFlashSACRunnerCfg",
    },
)

gym.register(
    id="DDT-Velocity-Flat-Tita-My-Play-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": base_env_cfg.MyTitaFlatEnvCfg_PLAY,
        "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:TitaFlatEstimatorPPORunnerCfg",
        "flash_sac_cfg_entry_point": f"{agents.__name__}.flash_sac_cfg:TitaFlatFlashSACRunnerCfg",
    },
)

gym.register(
    id="DDT-Velocity-Flat-Tita-Jump-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": jump_env_cfg.TitaJumpEnvCfg,
        "np3o_cfg_entry_point": f"{agents.__name__}.np3o_cfg:tita_flat_np3o_runner_cfg",
    },
)

gym.register(
    id="DDT-Velocity-Flat-Tita-Jump-Play-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": jump_env_cfg.TitaJumpEnvCfg_PLAY,
        "np3o_cfg_entry_point": f"{agents.__name__}.np3o_cfg:tita_flat_np3o_runner_cfg",
    },
)

gym.register(
    id="DDT-Velocity-Rough-Tita-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": rough_env_cfg.TitaRoughEnvCfg,
        "np3o_cfg_entry_point": f"{agents.__name__}.np3o_cfg:tita_rough_np3o_runner_cfg",
    },
)

gym.register(
    id="DDT-Velocity-Rough-Tita-Play-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": rough_env_cfg.TitaRoughEnvCfg_PLAY,
        "np3o_cfg_entry_point": f"{agents.__name__}.np3o_cfg:tita_rough_np3o_runner_cfg",
    },
)
