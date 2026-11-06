# TITA sit/stand: standing first, low heights after 20000 steps

Execution Domain: TRAINING_SIM / VALIDATION_SIM / DESKTOP_DRY_RUN

Evidence Status: PASS (configuration, exact phase boundary, finite native training); NOT_TESTED (trained balance and sitting/rising success).

Policy Checkpoint SHA256: f639dc1f3e273aa790be272f176a81509a002915fbfa2c9423957b3feb6a2d6a (independent accelerated boundary verification policy).

Main experiment checkpoint SHA256: PENDING (new policy, first checkpoint at 5000 steps).

## Changes and active experiment

The user observed immediate falls. Previous experiment `tita_mjlab_092054_548869` was intentionally interrupted at step 19670. Its last saved model_15000 hash is `6c173ea4f0cf91e193bddda8af766152f93aea160c4fb39d6d2e71ce9e8e3da1`. The trainer reports KeyboardInterrupt as FAIL; that run was stopped for replacement, not continued.

New experiment `tita_mjlab_095950_402808` starts FROM SCRATCH with no --resume or --warm_start. FlashSAC, 4096 environments, 100000 vector steps, W&B online, checkpoints every 5000 and 40 s videos every 10000.

W&B: https://forge.coreweave.com/wandb/bjy6614-postech/tita_flat_flash_sac/runs/gystjcqy

Main checkpoint directory: `mj_lab/logs/flash_sac/tita_mjlab_095950_402808/`.

| Training vector step | Height goals | Base/knee force >1 N termination |
| --- | --- | --- |
| 1–19999 | 0.25–0.50 m, uniform with inherited nominal-goal fraction | Enabled |
| 20000 onward | 0.07–0.50 m, alternating low/high targets with ramps across intermediate heights | Disabled |

Forty-second timeout remains active in both stages. Height command speed remains 0.04 m/s, roll/pitch rates 0.15 rad/s. Widened IDLE-reaching action gains, PD gains/torque caps and all DR settings are preserved.

Stage 1 uses original flat joint deviation and knee contact cost coefficients at all goals, with no low-height motion gate. Stage 2 restores the existing emitted-height gate (zero motion/costs below 0.20 m, linearly restored by 0.27 m). Roll/pitch retain rate limits when settling toward zero. No reward terms were added.

Before transition 20000, the trainer updates the live command sampler and saved config together, empties replay and pending n-step transitions, resets all environments, per-episode returns/lengths and the reward normalizer's per-episode return accumulator. It keeps the same actor, critic, optimizer, global learner count and running normalization statistics. During replay refill it uses the learned policy. New-stage transitions cannot accumulate n-step returns with old-stage ones. The transition is keyed to global vector steps, independent of episode resets and optimizer update counts.

Curriculum stage and transition step are saved in the native config. Playback stays at the checkpoint's saved stage even though its local simulation counter starts at zero; resumed training uses the saved global checkpoint step. Older checkpoints without a curriculum schedule retain their saved MDP. W&B records stage, contact-termination flag and minimum goal height.

Latest observed main step: 200; updates: 348; stage: 1; contact terminations on this observed step: 295. Initial episodes can still fall while learning; the new early termination resets them promptly.

## Executed checks

- `pytest -q test/test_mjlab_sit_stand.py test/test_mjlab_roll_pitch_height.py test/test_sim2sim_pose.py test/test_mjlab_support_velocity.py`: PASS, 36 tests and 14 subtests. Includes exact 19999/20000 boundary, actual force-history threshold behavior, live sampler update, saved stage persistence, original-task regression and native CUDA checks. Two inherited body_mass/inertia warnings were left unchanged.
- `test/check_sit_stand_curriculum.py`: PASS, real FlashSAC and native CUDA physics with 4096 environments, 16 vector steps and 12 finite updates. Only the probe shortens the switch to step 8. Verified one learner, unchanged weights at boundary, replay/n-step cleared, policy used while replay refills, stage-1/2 checkpoints saved correctly and production switch remains 20000. The final replay contains exactly 7*4096 new-stage transitions. This does not establish learned balance quality.
- `./scripts/agent-check.sh`: PASS, 756 Python syntax checks and 8 URDF parses.
- Final incremental diff inspected: PASS; no unrelated files modified or deleted. Existing dirty work preserved. See `sit_stand_curriculum_changes.diff` and `sit_stand_curriculum_diff_audit.json`.

## Changed files

- `mj_lab/robots/tita/sit_stand_env_cfg.py`: stage-dependent targets and contact termination; original penalties in standing pretraining.
- `mj_lab/scripts/train.py`: exact vector-step transition, replay/reset handling, persistence and metrics.
- `test/test_mjlab_sit_stand.py`: stage boundary/contact/sampler/serialization regressions.
- `test/check_sit_stand_curriculum.py`: real native/learner transition probe.

## Remaining limits

20000 steps is a fixed switch requested for this experiment; standing proficiency at that point is not yet established. Successful low-height rising remains untested. The 0.07 m goal is soft because upright base geometry contacts the ground near 0.079 m. No hardware commands or deployment were performed.

Current branch: `agent/codex/tita-walk`. No commit, push or PR.
