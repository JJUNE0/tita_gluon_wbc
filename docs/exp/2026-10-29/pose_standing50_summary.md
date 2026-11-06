# Diverse-pose stationary training 50%, height penalty -50

Execution Domain: TRAINING_SIM / DESKTOP_DRY_RUN

Evidence Status: PASS (configuration, sampler/contract regressions, native finite learning and experiment startup); NOT_TESTED (trained stationary/pose quality).

Policy Checkpoint SHA256: 483bb5ffe561bcd4fe59f7303ae5c1de9d862f173f15ae4777c1e3ccbd656b52 (independent native curriculum probe, not used to initialize the main run).

Main policy checkpoint SHA256: PENDING until first scheduled save.

## Authorized changes

User approved the proposed 50% zero-velocity training with varied pose goals and base_height_l2 weight -10 -> -50, and requested immediate training.

- Velocity resampling every 6–8 s chooses all-zero vx/vy/yaw target with probability 0.5 rather than 0.1. It is a probabilistic mix across all environments, not a permanently assigned cohort; every environment practices movement/stop transitions. The remaining targets retain saved vx/yaw ranges (+/-1.5 m/s and +/-3 rad/s, vy=0).
- Pose target sampling remains independent: the zero-velocity samples include diverse roll/pitch/height, not only the nominal stance. Roll +/-30 deg and pitch +/-15 deg at high goals are retained. Existing nominal-goal mixing is retained. At low goals, roll/pitch remain zero and velocity is gated as before. That low-height gate can make the emitted zero-command fraction exceed 50%; the 50% value refers to sampled velocity targets.
- Height squared-error coefficient is -50 throughout both curriculum stages. For an upright robot at 5 cm error, weighted kernel becomes -0.125 instead of -0.025 before the manager's dt factor; same 5x scaling at other errors. No reward terms or other weights were added/changed.

The existing curriculum is retained: before 20000 vector steps height range 0.25–0.50 m with base/knee contact termination enabled; from 20000 height range 0.07–0.50 m, alternating low/high target bands and contact termination disabled. Forty-second timeout and the boundary replay/n-step reset remain. This task did not implement the separately discussed height-dependent contact-termination proposal.

Height rate 0.04 m/s, roll/pitch rates 0.15 rad/s, action envelope, PD gains, caps, friction/mass/inertia/COM/delay/knee-gain DR, pose-aware stop-state ordering and velocity-qualified moving anchor remain unchanged. Actor/critic/action dimensions 38/42/8; shared FlashSAC algorithm unchanged. Earlier checkpoints keep their saved settings.

## Active experiment

New run: `tita_mjlab_163655_667608`.

Initialization: FROM SCRATCH; --resume and --warm_start are null. Fresh actor/critic, optimizer, replay, normalization and counters. No historical good policy, 100k policy or validation-probe checkpoint was loaded.

- 4096 environments, target 100000 vector steps, seed 42.
- W&B online: https://forge.coreweave.com/wandb/bjy6614-postech/tita_flat_flash_sac/runs/sy9trvq6.
- Checkpoint directory: `mj_lab/logs/flash_sac/tita_mjlab_163655_667608/`; saves every 5000.
- Forty-second videos every 10000 with velocity and pose target/emitted/actual overlays; first upload not yet due.
- Latest observed step 200, learner updates 348, stage 1; all observed learner metrics finite.
- Console: `pose_standing50_training.log`; invocation/provenance: `pose_standing50_launch.json` and `tita_mjlab_163655_667608_args.json`.

The earlier 100k experiment had already completed; no old TITA training needed interruption. Other active workspace GPU jobs were preserved; GPU was already busy at launch.

## Executed verification

1. `pytest -q test/test_mjlab_sit_stand.py test/test_pose_stop_latch.py test/test_mjlab_roll_pitch_height.py test/test_sim2sim_pose.py`: PASS, 35 tests and 14 subtests. Includes 10000-sample phase-1/2 50% stop statistics, varied nonzero roll/pitch and height among stopped samples, nominal-pose inclusion, low-height tilt zeroing, move-to-stop and stop-to-move transitions, native/adapter latch parity and existing task regressions. Three inherited mass/inertia DR warnings were not altered. Log: `pose_standing50_tests.log`.
2. Real native mjlab/FlashSAC probe, 4096 environments, 16 vector steps and 12 finite updates: PASS. Only the probe switches at step 8; production remains 20000. Confirmed both saved curriculum-stage checkpoints retain rel_standing_envs=0.5 and height weight=-50, and existing weights-preserving transition/replay reset still passes. Probe: `/home/cocel/Desktop/Research/tita_gluon_wbc/mj_lab/logs/flash_sac/tita_mjlab_163542_137760/model_16`; results `pose_standing50_native_probe.json`.
3. `./scripts/agent-check.sh`: PASS; log `pose_standing50_agent_check.log`.
4. Final incremental diff reviewed: `pose_standing50_changes.diff`; no unrelated modified/deleted files in `pose_standing50_diff_audit.json`. Pre-existing dirty work preserved.

## Changed files

- `mj_lab/robots/tita/sit_stand_env_cfg.py`: two scoped configuration changes plus rationale comments.
- `test/test_mjlab_sit_stand.py`: inheritance expectations and actual sampler/pose/transition regressions.
- `test/check_sit_stand_curriculum.py`: verifies both saved stages retain the new settings.

## Limits

This proves the intended experiment is running with the requested settings, not that the new policy already resolves drift or arbitrary-pose standing. The prior fixed 20000 switch and global post-switch contact-termination behavior remain possible contributors to instability and should be evaluated on new saved policies. The 0.07 m height goal remains soft relative to the approximately 0.079 m base collision floor.

No physical robot commands, deployment or Git publication. Current branch: `agent/codex/tita-walk`.
