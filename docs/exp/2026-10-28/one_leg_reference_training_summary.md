# Fixed-side one-leg balance with operator pose guidance

Execution Domains: TRAINING_SIM, VALIDATION_SIM, DESKTOP_DRY_RUN.

Evidence Status: PASS for scoped tests, finite learner updates, checkpoint/export/video plumbing and simulation startup. Learned one-leg balance remains NOT_TESTED for the new run.

Policy Checkpoint SHA256: new full experiment's first checkpoint is pending. The separate 40-step pipeline probe used `9e581ebc10b423575f35b9d71323bf76b77e35e0ceb051edd38ab59093ac6a59`.

Branch: `agent/codex/tita-walk`.

## Motivation and reference interpretation

The old run's logged mean episode durations averaged 2.48688 s in the 15k–20k window and 2.505824 s in the 25k–30k window. All sampled timeout log entries in those windows were zero. Its last logged episode mean before interruption was 2.9338 s. This is evidence of poor progress toward long support, but timeout alone neither proves a particular reward bug nor measures actual single-leg success.

Old `gait_support` already supplied positive reward for double support before the requested swing. The old unsatisfied swing score could be -2 per second of simulated time, while the termination weight -10 is timestep-scaled to -0.2 per failure at 50 Hz. Missing an explicit alive term is not the only possible cause; the scheduled mode transition and sparse successful lift experience also matter. No causal claim is made that the policy deliberately sought resets.

The operator-authored RViz example is retained at `stand_one_leg_operator_reference.json`, SHA256 `58b31faa343f8360a2b0d5be5b904731bde97faa76579eddda0911225b8aca8d`. It had about 32 degrees body roll and approximately 43–45 degrees leg_1 angles. It was a kinematic style reference, with neither COM equilibrium nor actual ground support established. Accordingly, the new task rewards broad angle magnitudes and leaves their signs free; it does not force the full recorded pose, use its wheel rotation values, or reset the robot into that pose.

## New task

`--task stand_one_leg_reference` is an additive task. Older alternating `stand_one_leg` configuration and functions are preserved for replay.

- Left wheel supports and right wheel lifts throughout the episode. No gait command, phase observation, alternation, settling clock or reward mode switch is present.
- Base vx/vy/yaw commands are zero. Both wheel velocity actions remain enabled with the existing scales, gains and torque limits.
- Starts at nominal two-foot joint configuration, with zero base/joint reset velocities. Policy control and the fixed target apply from the first step; this is not a new two-second warmup stage.
- Actor/critic/action dimensions: 35/39/8. The five gait inputs are absent. The new run does not reuse the old 40-input network.
- Delay, gain, knee-output, friction, mass/inertia/CoM and interval-push randomization remain enabled. Base/knee contacts terminate throughout.
- `sim_reset_on_policy_entry=true` is stored explicitly so simulation policy entry starts at the saved nominal standing state even without a gait command. Existing sim2sim code already honors that flag; no ROS runtime code was changed.

| Reward | Weight | Behavior |
| --- | ---: | --- |
| alive | +2 | Every non-failure step; timeout is not failure |
| single_support | +2 | Left contact times right clearance/4 cm, clipped to [0,1], minus 0.25 for right contact and 1 for missing left contact |
| pose_hint | +0.5 | Gradual progress toward roll magnitude 20–40 deg and both leg_1 magnitudes 25–40 deg; credit fades above the ranges |
| support_leg_tilt | -1 | Soft left hip-to-wheel vertical preference |
| stationary | -0.5 | World planar speed squared plus 0.1 times world-Z angular speed squared |
| action_rate | -0.005 | Same action-change cost as the previous standing task |
| dof_acc_l2 | -2.5e-7 | One acceleration cost over all eight joints |
| termination | -10 | Same failure cost as before |

All weights are multiplied by the 0.02 s control timestep. Before other costs, ordinary double contact earns +1.5 in weighted reward units (+0.03 per tick); correct 4 cm single support earns +4, with up to +0.5 additional pose credit. Thus both-foot standing remains worth preserving while supported lift earns more. These are soft incentives, not angle-based termination rules or hard joint targets.

Pose progress is the mean of three bounded angle scores, gated by left support. Below each preferred band, score grows linearly from zero. Above the upper edge, it fades with a 15-degree Gaussian width. Sagittal leg_2/leg_3 joints and wheel positions are not imitated. The reference is deliberately weak relative to actual support/clearance reward.

Separate episode metrics log true single-support fraction, total single-support seconds, double-contact fraction, peak right-wheel clearance and pose-hint score. True single support requires left contact, no right contact, right clearance at least 1 cm, and no failure termination. Total seconds are cumulative, not the longest continuous hold. A two-foot timeout must not be reported as one-leg success.

## Experiment transition

After successful validation, the user-authorized replacement stopped PID 1330530 with SIGINT at **37,273 steps / 74,346 updates**. Preserved last complete checkpoint: `mj_lab/logs/flash_sac/tita_mjlab_151340_019495/model_35000`, SHA256 `e5c07105c64c0e088b01566ea652acc2c03a43eab46831b32cb61b2c159b3b4b`. The generic trainer records FAIL/KeyboardInterrupt for this intentional interruption; `one_leg_reference_previous_stop.json` records its cause and verified process exit.

New run: `tita_mjlab_155513_268911`.

W&B: https://forge.coreweave.com/wandb/bjy6614-postech/tita_flat_flash_sac/runs/nf8gmjx0

PID: `1366252`; tmux: `mjlab_one_leg_reference_20261028_155510`.

Initialization: **FROM SCRATCH**, with `resume=null`, `warm_start=null`, and a new W&B run ID. New actor, critic, optimizers, normalization and replay. Budget: 100,000 vector steps, 1024 environments, seed 42, CUDA 0, two learner updates per step after replay warmup. W&B online; checkpoints every 5,000 steps; videos every 10,000 steps, 500 frames/10 s each.

Observed startup snapshot: **900 steps, 1,602 finite learner updates**. This proves startup, not standing quality. Full experiment's first checkpoint and scheduled video are pending at this snapshot.

Launch provenance/source hashes: `one_leg_reference_training_launch.json`; console: `one_leg_reference_training_console.log`; metrics: `tita_mjlab_155513_268911_metrics.jsonl`.

## Changes and executed validation

Changed files:

- Added `mj_lab/robots/tita/stand_one_leg_reference_env_cfg.py`.
- `mj_lab/scripts/train.py`: register the additional task.
- `mj_lab/checkpoint.py`: preserve the explicit simulation standing-entry flag.
- `mj_lab/README.md`: document the fixed support task, reward interpretation and success metrics.
- Added `test/test_mjlab_one_leg_reference.py`.
- Experiment evidence under `docs/exp/2026-10-28/`.

Executed tests/results:

- PASS: scoped fixed-reference + old single-leg + inline + flat/walk suite: **42 passed, 8 conditional skips**, `one_leg_reference_tests.log`. Includes actual CUDA physics, partial lift/wrong-side/airborne cases, pose-hint freedom, terminal vs timeout semantics, native metric logging, pickle roundtrip and playback schema.
- PASS: fresh 16-environment FlashSAC pipeline probe, 40 steps and **74 finite updates**, saved `tita_mjlab_155344_537072/model_40`; `one_leg_reference_learner_probe.log`. Probe is separate from the full experiment and not a balance result.
- PASS: three-frame native video encode/read path, `one_leg_reference_video_probe.json` and `.mp4`.
- PASS: actual checkpoint-to-ONNX export, 35 observations / 8 actions, 256-sample maximum absolute parity error **4.53e-6**; `one_leg_reference_sim2sim_prepare.log`.
- PASS: two actual ROS/MuJoCo/ONNX simulation startup cases with saved standing-entry reset, manual-key callbacks and headless flow; `one_leg_reference_sim2sim_runtime.json`. These use local ROS domain 90; passive GUI creation alone is suppressed in the manual scenario. No hardware execution.
- PASS: source verification preserves all unrelated shared/task sources; `one_leg_reference_source_verification.json`.
- Repository checks and incremental diff: `one_leg_reference_agent_check.log` and `one_leg_reference_changes.diff`.

Unresolved risks: explicit survival can encourage stable two-foot standing before lift is learned; pose guidance does not establish static feasibility or robustness. The vertical-leg preference remains soft and can compete with body/leg angle preferences. Successful sustained one-leg support must be established from later frozen rollouts and support-time metrics. No physical robot command, deployment, commit or publication was performed.
