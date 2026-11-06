"""Real-to-sim robustness variants of DDT-Velocity-Flat-Tita-My-v0 (same policy interface).

Registered from this sub-package so the existing TITA task registry stays untouched;
``ddt_lab.tasks`` imports all sub-packages through ``import_packages``.
"""

import gymnasium as gym

from .. import agents
from . import env_cfg

_AGENT_ENTRY_POINTS = {
    "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:TitaFlatEstimatorPPORunnerCfg",
    "flash_sac_cfg_entry_point": f"{agents.__name__}.flash_sac_cfg:TitaFlatFlashSACRunnerCfg",
}

gym.register(
    id="DDT-Velocity-Flat-Tita-My-Real2Sim-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    disable_env_checker=True,
    kwargs={"env_cfg_entry_point": env_cfg.MyTitaFlatReal2SimEnvCfg, **_AGENT_ENTRY_POINTS},
)

gym.register(
    id="DDT-Velocity-Flat-Tita-My-Real2Sim-BaseCom-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    disable_env_checker=True,
    kwargs={"env_cfg_entry_point": env_cfg.MyTitaFlatReal2SimBaseComEnvCfg, **_AGENT_ENTRY_POINTS},
)

# CoM-only arm: no actuator/friction change (see MyTitaFlatBaseComShiftEnvCfg).
gym.register(
    id="DDT-Velocity-Flat-Tita-My-BaseComShift-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    disable_env_checker=True,
    kwargs={"env_cfg_entry_point": env_cfg.MyTitaFlatBaseComShiftEnvCfg, **_AGENT_ENTRY_POINTS},
)

# Arm B: R1 actuator/friction events plus the same base CoM shift as arm A.
gym.register(
    id="DDT-Velocity-Flat-Tita-My-Real2Sim-BaseComShift-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    disable_env_checker=True,
    kwargs={"env_cfg_entry_point": env_cfg.MyTitaFlatReal2SimBaseComShiftEnvCfg, **_AGENT_ENTRY_POINTS},
)

# Arm B': B with 50 % nominal leg strength and a CoM x range that includes the URDF value.
gym.register(
    id="DDT-Velocity-Flat-Tita-My-Real2Sim-NomMix-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    disable_env_checker=True,
    kwargs={"env_cfg_entry_point": env_cfg.MyTitaFlatReal2SimNominalMixEnvCfg, **_AGENT_ENTRY_POINTS},
)

# Arms C1/C2: leg output scale around the identified ~0.65 and base CoM near URDF (C1); C2 adds
# vendor-stand zero-command shaping.
gym.register(
    id="DDT-Velocity-Flat-Tita-My-LegScale-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    disable_env_checker=True,
    kwargs={"env_cfg_entry_point": env_cfg.MyTitaFlatLegScaleEnvCfg, **_AGENT_ENTRY_POINTS},
)

gym.register(
    id="DDT-Velocity-Flat-Tita-My-LegScale-Reward-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    disable_env_checker=True,
    kwargs={"env_cfg_entry_point": env_cfg.MyTitaFlatLegScaleRewardEnvCfg, **_AGENT_ENTRY_POINTS},
)

# A80k successor: URDF CoM, wheel-odometry position-error observation (34 obs), leg MA2 in the loop,
# knee-only 92/2.3 with knee output-scale randomization.
gym.register(
    id="DDT-Velocity-Flat-Tita-My-PosKneeMA2-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    disable_env_checker=True,
    kwargs={"env_cfg_entry_point": env_cfg.MyTitaFlatPosKneeMA2EnvCfg, **_AGENT_ENTRY_POINTS},
)

# 2026-10-18 posma2 yaw review: point-contact (sphere) wheels on top of PosKneeMA2 (exp 1), the same
# without leg MA2 (exp 2), and exp 1 with lin_vel_x +-1.5 / ang_vel_z +-3.0 commands (exp 3).
gym.register(
    id="DDT-Velocity-Flat-Tita-My-PosKneeMA2-Sphere-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    disable_env_checker=True,
    kwargs={"env_cfg_entry_point": env_cfg.MyTitaFlatPosKneeMA2SphereEnvCfg, **_AGENT_ENTRY_POINTS},
)

gym.register(
    id="DDT-Velocity-Flat-Tita-My-PosKnee-Sphere-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    disable_env_checker=True,
    kwargs={"env_cfg_entry_point": env_cfg.MyTitaFlatPosKneeSphereEnvCfg, **_AGENT_ENTRY_POINTS},
)

gym.register(
    id="DDT-Velocity-Flat-Tita-My-PosKneeMA2-Sphere-Fast-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    disable_env_checker=True,
    kwargs={"env_cfg_entry_point": env_cfg.MyTitaFlatPosKneeMA2SphereFastEnvCfg, **_AGENT_ENTRY_POINTS},
)

# Exp 4: exp 3 (sphere wheels, +-1.5 m/s, +-3.0 rad/s) without leg MA2.
gym.register(
    id="DDT-Velocity-Flat-Tita-My-PosKnee-Sphere-Fast-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    disable_env_checker=True,
    kwargs={"env_cfg_entry_point": env_cfg.MyTitaFlatPosKneeSphereFastEnvCfg, **_AGENT_ENTRY_POINTS},
)

# Exp 5: PosKneeMA2 (cylinder wheels, default commands) without leg MA2.
gym.register(
    id="DDT-Velocity-Flat-Tita-My-PosKnee-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    disable_env_checker=True,
    kwargs={"env_cfg_entry_point": env_cfg.MyTitaFlatPosKneeEnvCfg, **_AGENT_ENTRY_POINTS},
)

# Exp 3 + zero-command heading drift reward and critic heading error (policy interface unchanged).
gym.register(
    id="DDT-Velocity-Flat-Tita-My-PosKneeMA2-Sphere-Fast-Heading-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    disable_env_checker=True,
    kwargs={"env_cfg_entry_point": env_cfg.MyTitaFlatPosKneeMA2SphereFastHeadingEnvCfg, **_AGENT_ENTRY_POINTS},
)

# Heading run with the gyro heading error also in the actor (35 policy observations).
gym.register(
    id="DDT-Velocity-Flat-Tita-My-PosKneeMA2-Sphere-Fast-HeadingObs-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    disable_env_checker=True,
    kwargs={"env_cfg_entry_point": env_cfg.MyTitaFlatPosKneeMA2SphereFastHeadingObsEnvCfg, **_AGENT_ENTRY_POINTS},
)

# No-MA2 heading run: experiment 2 (sphere, no MA2, default commands) + the same heading reward/observations.
gym.register(
    id="DDT-Velocity-Flat-Tita-My-PosKnee-Sphere-HeadingObs-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    disable_env_checker=True,
    kwargs={"env_cfg_entry_point": env_cfg.MyTitaFlatPosKneeSphereHeadingObsEnvCfg, **_AGENT_ENTRY_POINTS},
)

# No-MA2 heading run without the 1 s heading warmup (reward anchor and observation start at the stop).
gym.register(
    id="DDT-Velocity-Flat-Tita-My-PosKnee-Sphere-HeadingObsW0-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    disable_env_checker=True,
    kwargs={"env_cfg_entry_point": env_cfg.MyTitaFlatPosKneeSphereHeadingObsW0EnvCfg, **_AGENT_ENTRY_POINTS},
)
