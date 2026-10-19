"""Gym registration for fixed- and moving-arm TITA+GLUON MOO stages."""

import gymnasium as gym

from . import agents
from .env_cfg import (
    TitaGluonCurriculumArmFlatEnvCfg,
    TitaGluonCurriculumArmFlatEnvCfg_PLAY,
    TitaGluonFlatEnvCfg,
    TitaGluonFlatEnvCfg_PLAY,
    TitaGluonInspectionCurriculumArmFlatEnvCfg,
    TitaGluonInspectionCurriculumArmFlatEnvCfg_PLAY,
    TitaGluonRandomArmFlatEnvCfg,
    TitaGluonRandomArmFlatEnvCfg_PLAY,
    TitaGluonSequentialInspectionFlatEnvCfg,
    TitaGluonSequentialInspectionFlatEnvCfg_PLAY,
)


gym.register(
    id="Isaac-Velocity-Flat-Tita-Gluon-InspectionCurriculumArm-RMATeacher-v0-moo-ppo",
    entry_point="ddt_lab.envs:ManagerBasedMOORLEnv",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": TitaGluonInspectionCurriculumArmFlatEnvCfg,
        "co_rl_cfg_entry_point": agents.TitaGluonInspectionCurriculumArmRMATeacherRunnerCfg,
    },
)

gym.register(
    id="Isaac-Velocity-Flat-Tita-Gluon-InspectionCurriculumArm-Play-v0-moo-ppo",
    entry_point="ddt_lab.envs:ManagerBasedMOORLEnv",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": TitaGluonInspectionCurriculumArmFlatEnvCfg_PLAY,
        "co_rl_cfg_entry_point": agents.TitaGluonInspectionCurriculumArmRMATeacherRunnerCfg,
    },
)


gym.register(
    id="Isaac-Velocity-Flat-Tita-Gluon-CurriculumArm-RMATeacher-TargetHeight-v0-moo-ppo",
    entry_point="ddt_lab.envs:ManagerBasedMOORLEnv",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": TitaGluonCurriculumArmFlatEnvCfg,
        "co_rl_cfg_entry_point": agents.TitaGluonCurriculumArmRMATeacherRunnerCfg,
    },
)

gym.register(
    id="Isaac-Velocity-Flat-Tita-Gluon-CurriculumArm-Play-v0-moo-ppo",
    entry_point="ddt_lab.envs:ManagerBasedMOORLEnv",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": TitaGluonCurriculumArmFlatEnvCfg_PLAY,
        "co_rl_cfg_entry_point": agents.TitaGluonCurriculumArmRMATeacherRunnerCfg,
    },
)


gym.register(
    id="Isaac-Velocity-Flat-Tita-Gluon-GTBaseVel-TargetHeight-v0-moo-ppo",
    entry_point="ddt_lab.envs:ManagerBasedMOORLEnv",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": TitaGluonFlatEnvCfg,
        "co_rl_cfg_entry_point": agents.TitaGluonMOOPPORunnerCfg,
    },
)

gym.register(
    id="Isaac-Velocity-Flat-Tita-Gluon-RandomArm-GTBaseVel-TargetHeight-v0-moo-ppo",
    entry_point="ddt_lab.envs:ManagerBasedMOORLEnv",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": TitaGluonRandomArmFlatEnvCfg,
        "co_rl_cfg_entry_point": agents.TitaGluonRandomArmMOOPPORunnerCfg,
    },
)

gym.register(
    id="Isaac-Velocity-Flat-Tita-Gluon-RandomArm-Play-v0-moo-ppo",
    entry_point="ddt_lab.envs:ManagerBasedMOORLEnv",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": TitaGluonRandomArmFlatEnvCfg_PLAY,
        "co_rl_cfg_entry_point": agents.TitaGluonRandomArmMOOPPORunnerCfg,
    },
)

gym.register(
    id="Isaac-Velocity-Flat-Tita-Gluon-Play-v0-moo-ppo",
    entry_point="ddt_lab.envs:ManagerBasedMOORLEnv",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": TitaGluonFlatEnvCfg_PLAY,
        "co_rl_cfg_entry_point": agents.TitaGluonMOOPPORunnerCfg,
    },
)

gym.register(
    id="Isaac-Velocity-Flat-Tita-Gluon-SequentialInspection-v0-moo-ppo",
    entry_point="ddt_lab.envs:ManagerBasedMOORLEnv",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": TitaGluonSequentialInspectionFlatEnvCfg,
        "co_rl_cfg_entry_point": agents.TitaGluonCurriculumArmRMATeacherRunnerCfg,
    },
)

gym.register(
    id="Isaac-Velocity-Flat-Tita-Gluon-SequentialInspection-Play-v0-moo-ppo",
    entry_point="ddt_lab.envs:ManagerBasedMOORLEnv",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": TitaGluonSequentialInspectionFlatEnvCfg_PLAY,
        "co_rl_cfg_entry_point": agents.TitaGluonCurriculumArmRMATeacherRunnerCfg,
    },
)
