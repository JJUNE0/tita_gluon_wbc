# Copyright (c) 2022-2025, The Isaac Lab Project Developers (https://github.com/isaac-sim/IsaacLab/blob/main/CONTRIBUTORS.md).
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

import gymnasium as gym

from . import agents, flat_env_cfg, jump_env_cfg, my_flat_env_cfg, rough_env_cfg

##
# Register Gym environments. All Tita tasks are wired to NP3O (BarlowTwins-PPO);
# stock PPO is no longer supported because the policy obs is now 3D.
##

gym.register(
    id="DDT-Velocity-Flat-Tita-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": flat_env_cfg.TitaFlatEnvCfg,
        "np3o_cfg_entry_point": f"{agents.__name__}.np3o_cfg:tita_flat_np3o_runner_cfg",
    },
)

gym.register(
    id="DDT-Velocity-Flat-Tita-Play-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": flat_env_cfg.TitaFlatEnvCfg_PLAY,
        "np3o_cfg_entry_point": f"{agents.__name__}.np3o_cfg:tita_flat_np3o_runner_cfg",
    },
)

gym.register(
    id="DDT-Velocity-Flat-Tita-My26-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": my_flat_env_cfg.MyTitaFlatV26EnvCfg,
        "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:TitaFlatEstimatorPPORunnerCfg",
    },
)

gym.register(
    id="DDT-Velocity-Flat-Tita-My26-Play-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": my_flat_env_cfg.MyTitaFlatV26EnvCfg_PLAY,
        "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:TitaFlatEstimatorPPORunnerCfg",
    },
)

gym.register(
    id="DDT-Velocity-Flat-Tita-My27-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": my_flat_env_cfg.MyTitaFlatV27EnvCfg,
        "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:TitaFlatEstimatorPPORunnerCfg",
    },
)

gym.register(
    id="DDT-Velocity-Flat-Tita-My27-Play-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": my_flat_env_cfg.MyTitaFlatV27EnvCfg_PLAY,
        "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:TitaFlatEstimatorPPORunnerCfg",
    },
)

gym.register(
    id="DDT-Velocity-Flat-Tita-My28-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": my_flat_env_cfg.MyTitaFlatV28EnvCfg,
        "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:TitaFlatEstimatorPPORunnerCfg",
    },
)

gym.register(
    id="DDT-Velocity-Flat-Tita-My28-Play-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": my_flat_env_cfg.MyTitaFlatV28EnvCfg_PLAY,
        "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:TitaFlatEstimatorPPORunnerCfg",
    },
)

gym.register(
    id="DDT-Velocity-Flat-Tita-My29-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": my_flat_env_cfg.MyTitaFlatV29EnvCfg,
        "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:TitaFlatEstimatorPPORunnerCfg",
    },
)

gym.register(
    id="DDT-Velocity-Flat-Tita-My29-Play-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": my_flat_env_cfg.MyTitaFlatV29EnvCfg_PLAY,
        "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:TitaFlatEstimatorPPORunnerCfg",
    },
)

gym.register(
    id="DDT-Velocity-Flat-Tita-My30-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": my_flat_env_cfg.MyTitaFlatV30EnvCfg,
        "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:TitaFlatEstimatorPPORunnerCfg",
    },
)

gym.register(
    id="DDT-Velocity-Flat-Tita-My30-Play-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": my_flat_env_cfg.MyTitaFlatV30EnvCfg_PLAY,
        "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:TitaFlatEstimatorPPORunnerCfg",
    },
)

gym.register(
    id="DDT-Velocity-Flat-Tita-My31-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": my_flat_env_cfg.MyTitaFlatV31EnvCfg,
        "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:TitaFlatEstimatorPPORunnerCfg",
    },
)

gym.register(
    id="DDT-Velocity-Flat-Tita-My31-Play-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": my_flat_env_cfg.MyTitaFlatV31EnvCfg_PLAY,
        "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:TitaFlatEstimatorPPORunnerCfg",
    },
)

gym.register(
    id="DDT-Velocity-Flat-Tita-My32-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": my_flat_env_cfg.MyTitaFlatV32EnvCfg,
        "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:TitaFlatEstimatorPPORunnerCfg",
    },
)

gym.register(
    id="DDT-Velocity-Flat-Tita-My32-Play-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": my_flat_env_cfg.MyTitaFlatV32EnvCfg_PLAY,
        "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:TitaFlatEstimatorPPORunnerCfg",
    },
)

gym.register(
    id="DDT-Velocity-Flat-Tita-My33-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": my_flat_env_cfg.MyTitaFlatV33EnvCfg,
        "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:TitaFlatEstimatorPPORunnerCfg",
    },
)

gym.register(
    id="DDT-Velocity-Flat-Tita-My33-Play-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": my_flat_env_cfg.MyTitaFlatV33EnvCfg_PLAY,
        "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:TitaFlatEstimatorPPORunnerCfg",
    },
)

gym.register(
    id="DDT-Velocity-Flat-Tita-My34-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": my_flat_env_cfg.MyTitaFlatV34EnvCfg,
        "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:TitaFlatEstimatorPPORunnerCfg",
    },
)

gym.register(
    id="DDT-Velocity-Flat-Tita-My34-Play-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": my_flat_env_cfg.MyTitaFlatV34EnvCfg_PLAY,
        "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:TitaFlatEstimatorPPORunnerCfg",
    },
)

for _v in [35, 36, 37, 38, 39]:
    gym.register(
        id=f"DDT-Velocity-Flat-Tita-My{_v}-v0",
        entry_point="isaaclab.envs:ManagerBasedRLEnv",
        disable_env_checker=True,
        kwargs={
            "env_cfg_entry_point": getattr(my_flat_env_cfg, f"MyTitaFlatV{_v}EnvCfg"),
            "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:TitaFlatEstimatorPPORunnerCfg",
        },
    )
    gym.register(
        id=f"DDT-Velocity-Flat-Tita-My{_v}-Play-v0",
        entry_point="isaaclab.envs:ManagerBasedRLEnv",
        disable_env_checker=True,
        kwargs={
            "env_cfg_entry_point": getattr(my_flat_env_cfg, f"MyTitaFlatV{_v}EnvCfg_PLAY"),
            "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:TitaFlatEstimatorPPORunnerCfg",
        },
    )

gym.register(
    id="DDT-Velocity-Flat-Tita-My40-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": my_flat_env_cfg.MyTitaFlatV40EnvCfg,
        "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:TitaFlatEstimatorPPORunnerCfg",
    },
)

gym.register(
    id="DDT-Velocity-Flat-Tita-My40-Play-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": my_flat_env_cfg.MyTitaFlatV40EnvCfg_PLAY,
        "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:TitaFlatEstimatorPPORunnerCfg",
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
