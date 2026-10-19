# TITA leg_1 symmetric default pose fix (FlashSAC My task)

Execution Domain: TRAINING_SIM (8-step smoke) / DESKTOP_DRY_RUN (kinematics check)

Policy Checkpoint SHA256: N/A (config fix; no new policy trained). Diagnosed checkpoint:
`tita_flash_sac_172127_928297/model_100000/actor.pt` = `3fd6113b95be69e0956f1510d4002dd161bc7226e0f1d9ade205117fc3edaed6`

Evidence Status: PASS for config wiring and smoke run. Full retraining and leg posture in Isaac/MuJoCo: NOT_TESTED.

## Problem

Both `joint_left_leg_1` and `joint_right_leg_1` have the same URDF origin rotation
(`rpy="1.5708 0 1.5708"`) and axis, so their axes are parallel, not mirrored.
`DDT_TITA_CFG` (inherited from DDT_Lab) sets leg_1 = (+0.1, +0.1), which is an
asymmetric pose. MuJoCo FK (leg_2=0.8, leg_3=-1.5), wheel position in base frame:

| leg_1 (L, R) | left wheel y / z | right wheel y / z |
|---|---|---|
| 0.0, 0.0 | 0.283 / -0.292 | -0.284 / -0.292 |
| +0.1, +0.1 | 0.312 / -0.271 | -0.253 / -0.310 |
| +0.1, -0.1 | 0.312 / -0.271 | -0.312 / -0.271 |

Run `tita_flash_sac_172127_928297` trained with leg_1 = (+0.1, +0.1) as its init
pose and action offset. `joint_deviation_hip` pulled toward that pose, and
`joint_mirror` penalized (q_L - q_R)^2, which also favors the same-direction pose.
The nominal MuJoCo rollout (`flash_leg_fixed_lqr4` A, seed 42) holds about -3.3 deg roll.
sim2sim reads defaults from the checkpoint `env.yaml`, so the asymmetry came from training.

## Changes

- `my_flat_env_cfg.py`: robot init_state leg_1 = (0.0, 0.0), task-scoped.
  `DDT_TITA_CFG` and `rough_env_cfg.py` are unchanged.
- `rewards.py` `joint_mirror`: optional `mirror_signs` (default +1 = old behavior);
  penalty is (q_L - sign * q_R)^2. Pairs accept explicit name lists (`preserve_order=True`).
- `my_flat_env_cfg.py` `joint_mirror`: explicit leg_1..3 lists, signs [-1, 1, 1].
- `flash_sac_cfg.py`: hip gains 3.2/2.4 -> 2.8/2.8 so hip targets stay at
  -0.7..+0.7 rad (soft limit +-0.707) about the new zero default.

## Evidence

- `./scripts/agent-check.sh`: PASS.
- Smoke: `scripts/flash_sac/train.py --task DDT-Velocity-Flat-Tita-My-v0 --num_envs 4 --steps 8 ...`
  exit 0, 10 learner updates, finite rewards (`leg1_symmetric_smoke.log`).
  Output run `tita_flash_sac_104528_287986`: env.yaml leg_1 = 0.0/0.0, `mirror_signs`
  [[-1, 1, 1]]; ddt.json gains 2.8/2.8 for hips.
