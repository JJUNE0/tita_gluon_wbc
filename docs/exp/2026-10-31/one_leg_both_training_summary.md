# Independent fixed-left and fixed-right one-leg training

Execution Domain: TRAINING_SIM

Evidence Status: SUSPICIOUS — full training in progress; startup/configuration/finite-update validation PASS; trained balance quality NOT_TESTED.

Policy Checkpoint SHA256 (both main policies): PENDING until first scheduled step-5000 checkpoints.

Baseline checkpoint SHA256: fe8ca785da4353b79ef0b5af37ca073495b2156fa72395d939c3171bef8d27dd

Validation checkpoint SHA256, left: 1477d3df7dfce8bd1cf4042a1bc48621b035ae146eaaf189781dc60c699a7cb2

Validation checkpoint SHA256, right: 6ece92980cb0cc44291eccbb6c5c2fde155a407fb6ad2247ed04381621c9efc8

User request: train the earlier successful fixed-left one-leg task to 100000 steps, and an independent mirrored fixed-right task to 100000 steps. Both start from scratch, consistent with the session preference. No checkpoint or optimizer is loaded. The original model_40000 actor remains unchanged.

Both runs preserve the original 1024-environment setting, seed 42, FlashSAC, 1M replay, 100000 minimum replay, batch 2048, two updates per vector step, 20-s episodes, original observation/action/PD/physics/reset randomization, and all reward weights. This is fixed support for a whole episode with zero vx/vy/yaw; no gait, left/right command switching or added observation. Actor/critic dimensions remain 35/39, actions 8.

Reward weights: alive +2; single_support +2; loose pose_hint +0.5; support_leg_tilt -1; stationary -0.5; action_rate -0.005; joint acceleration -2.5e-7; termination -10. The 4-cm swing clearance is a saturated reward target, not a hard maximum. The body and swing leg remain free to balance; the support hip-to-wheel line is encouraged to be vertical. Base and knee contact terminations remain enabled.

Changed files:

- mj_lab/robots/tita/stand_one_leg_reference_env_cfg.py: side-aware balance metrics with legacy default left; added TitaStandOneLegRightReferenceEnvCfg which changes only three reward and five metric side parameters.
- mj_lab/scripts/train.py: register stand_one_leg_reference_right.
- test/test_mjlab_one_leg_right_reference.py: right/wrong/double support, mirrored geometry/reward/metric equivalence, side-specific vertical axis, unchanged parent configuration, pickle and 35-D playback contract.
- Experiment evidence: docs/exp/2026-10-31/one_leg_*.

Verified before full training:

- pytest on fixed reference, new mirrored right reference and support-command tests: PASS, 14 tests; three existing mass/inertia DR warnings. Log one_leg_both_tests.log.
- Two concurrent fresh native CLI probes, each 1024 environments and a full 1M CUDA replay allocation: PASS, 16 vector steps / 11 finite updates each.
- Saved native config comparison: left exactly equals the saved 40k configuration; right differs only in the three reward and five metric support_side parameters. Both action mappings and dimensions match the old actor. one_leg_both_native_validation.json.
- Actual checkpoint-to-ONNX preparation: PASS, 35 observations / 8 actions, 256 parity samples; max absolute errors 4.92e-6 left and 4.05e-6 right. Logs one_leg_left_export_probe.log and one_leg_right_export_probe.log. Probes are setup validation, not learned-balance results.
- Compilation of all three changed Python files, whitespace and incremental diff inspection: PASS.
- Source hash audit: PASS, only the two scoped existing source files changed; no unrelated source edits or deletions. one_leg_both_change_audit.json.
- ./scripts/agent-check.sh: PASS; direct log one_leg_both_agent_check.log.

Main runs are concurrent in separate persistent tmux sessions. Observed GPU use after both began updating: 4.7 GB of 24 GB, utilization 100%.

| Support | Task | Run | Last observed step / updates | W&B |
|---|---|---|---:|---|
| left | stand_one_leg_reference | tita_mjlab_201526_016988 | 800 / 1402 | [online](https://forge.coreweave.com/wandb/bjy6614-postech/tita_flat_flash_sac/runs/s8fqfbo2) |
| right | stand_one_leg_reference_right | tita_mjlab_201526_001807 | 800 / 1402 | [online](https://forge.coreweave.com/wandb/bjy6614-postech/tita_flat_flash_sac/runs/a9wtsorc) |

left checkpoint directory: /home/cocel/Desktop/Research/tita_gluon_wbc/mj_lab/logs/flash_sac/tita_mjlab_201526_016988

left tmux session: tita_one_leg_left_100k_20261031

left console: /home/cocel/Desktop/Research/tita_gluon_wbc/docs/exp/2026-10-31/one_leg_left_training.log

right checkpoint directory: /home/cocel/Desktop/Research/tita_gluon_wbc/mj_lab/logs/flash_sac/tita_mjlab_201526_001807

right tmux session: tita_one_leg_right_100k_20261031

right console: /home/cocel/Desktop/Research/tita_gluon_wbc/docs/exp/2026-10-31/one_leg_right_training.log

Save schedule: checkpoints every 5000 steps; online W&B videos every 10000 steps, 2000 frames each. Logging differs from the old run only in descriptive run names and video length; the new inactive standing_height_only=False argument is also recorded. The right task name identifies the fixed support side in checkpoint metadata.

Full launch commands, run IDs, URLs, argument comparisons and observed startup metrics: one_leg_both_launch.json.

Limits: the short probes establish correct setup and finite execution, not sustained one-leg success. Left/right learned performance may differ and requires later checkpoint evaluation. No hardware commands, deployment, commit or publication.

Branch: agent/codex/tita-walk.
