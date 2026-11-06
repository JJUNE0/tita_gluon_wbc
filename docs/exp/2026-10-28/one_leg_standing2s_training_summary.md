# Single-leg startup diagnosis and two-second standing phase

Execution Domains: TRAINING_SIM, VALIDATION_SIM, DESKTOP_DRY_RUN.

Evidence Status: PASS for configuration fixes, scoped tests, simulation protocol checks and fresh training startup. Sustained balance and successful gait remain NOT_TESTED for the new policy.

Policy Checkpoint SHA256: N/A — new run has not saved its first checkpoint at this verification snapshot.

Diagnosed frozen model_30000 SHA256: `5ea13082ba391aced464ed95c97ef29ba5c677a1ba699778b979b0c180fd5c33`.

Previous retained model_35000 SHA256: `09d393a3eead5fc8fdeedeeb0d5a48bb5ddb9b541b248f8325ee6d458512e823`.

Branch: `agent/codex/tita-walk`.

## Confirmed issue

The user clarified that learning videos showed falling and repeated episode resets, and selected learning balance from an already-standing two-foot pose for the first 2 seconds.

The old gait already waited 1 second. In the final 5000-step logging window of the stopped run, the mean of logged episode-length means was approximately **0.261 s**, with **51 reward snapshots and 0 positive gait-support snapshots**. Episodes usually ended before entering gait. The earlier reward multiplied gait-support by the gait-enabled flag, so there was no positive standing reward during that initial interval; only regularization and termination costs were available there.

The inherited reset multiplied joint angles by independent values in [-0.5, 1] and sampled all initial base velocity components in [-0.5, 0.5]. Frozen 30k policy diagnostics used 32 native environments, 4 seconds, seed 42, saved noise and physical randomization. At reset, **27/32** environments had at least one joint outside its limits; mean initial linear speed was approximately 0.499 m/s. All 32 first policy episodes ended before 1 second, median approximately 0.25 s, and gait exposure was zero. With nominal joint angles/zero initial base velocity, that already-learned policy still failed quickly (median approximately 0.20 s). Thus extending the timer alone would not repair the learned policy.

Zero-action nominal PD diagnostics are controls, not trained balancing policies: saved randomized resets had a median first end near 0.34 s; nominal reset near 0.64 s. These measurements show that stable reset and usable reward feedback are needed; they do not prove that one factor alone caused all failures. Full results: `one_leg_startup_diagnosis.json` / `.log`; helper `test/diagnose_one_leg_startup.py`. Training-log analysis: `one_leg_startup_log_analysis.json`.

## Implemented and currently running

- Episode starts at nominal joint angles with zero base and joint velocities.
- For the first **2 seconds**, gait remains off. The policy still controls the robot and receives **+2 when both wheels contact the ground**, zero from that task term otherwise.
- After 2 seconds, the same combined contact/clearance term switches to the existing 2 s gait cycle, 0.5 s swing per foot. Contact mismatch penalties and the single-support vertical-leg cost apply as before.
- Stationary velocity cost, action-change cost, joint acceleration **-2.5e-7**, and termination **-10** remain unchanged. Total reward terms remain **six**.
- Base/knee contact termination stays active during the first two seconds; contacts are not ignored to hide falls.
- Motor delay, gain, knee-output, mass, inertia, CoM, friction and interval-push randomization remain enabled. Existing flat/walk/inline configs, shared MDP kernels and robot gains were preserved.

**The current warmup does not use the complete flat reward set.** It only changes the task reward to positive double contact during the first 2 s. Flat orientation, base-height, hip/shoulder deviation and flat velocity-tracking rewards are absent. The user subsequently proposed using flat's proven reward set during warmup and requested an explanation of current behavior; that further proposal has not been applied, and this run was not restarted again for it.

## sim2sim initialization alignment

The old interactive state machine hands control to the policy from a deeply folded SIT pose, while this task trains from the default standing state. New stationary, zero-command step-in-place checkpoint contracts record `sim_reset_on_policy_entry=true`. The exporter validates and preserves that optional boolean; the sim node resets physics to the checkpoint's default root/joint state once on policy entry, clears action/filter history and restarts the saved gait clock. This also applies to policy reentry.

Older checkpoints without the field retain their original startup behavior and settling time. This is a simulation reset matching the chosen already-standing task, not learned sit-to-stand and not a hardware control change.

The protocol integration test used a temporary copy of the already verified old 10k ONNX interface with only this flag and a 2 s settling time added. It proves control flow and first-observation reset alignment, not performance of the new policy. Provenance: `one_leg_standing_runtime_fixture_provenance.json`; results: `one_leg_standing_runtime_checks.json` / `.md` / `.log`. The actual first policy joint-position observation matched the saved nominal pose in both manual and headless cases.

## Experiment transition and active run

Stopped the previous failed-startup run at **37012 steps**, preserving `/home/cocel/Desktop/Research/tita_gluon_wbc/mj_lab/logs/flash_sac/tita_mjlab_142712_580757/model_35000`. Its generic raw result is FAIL/KeyboardInterrupt because the trainer uses that status for intentional interruption; this was the experiment replacement described in the conversation, not a numerical crash.

New run: `tita_mjlab_151340_019495`.

W&B: https://forge.coreweave.com/wandb/bjy6614-postech/tita_flat_flash_sac/runs/qm5sm7r4

PID `1330530`; tmux `mjlab_one_leg_standing2s_20261028_151336`.

Checkpoint directory: `mj_lab/logs/flash_sac/tita_mjlab_151340_019495`.

Initialization: **from scratch**, with `resume=null`, `warm_start=null`, `wandb_run_id=null`; fresh actor, critic, optimizers, normalizers and replay. Budget remains 100000 vector steps / 1024 environments / seed 42 / CUDA 0 / two updates per step. W&B online, checkpoint every 5000 steps and video every 10000 steps (500 frames).

Observed metrics / behavior / log summary at verification: step **4300**, **8402** finite updates. Source hashes match launch provenance. Positive combined support reward is now observed in early logs, but that includes the initial double-support reward and is not evidence of learned single-leg gait. Early episodes remain short while the fresh policy learns; no claim is made that it already survives 2 seconds.

Launch provenance: `one_leg_standing2s_training_launch.json`; console: `one_leg_standing2s_training_console.log`; metrics: `docs/exp/2026-10-28/tita_mjlab_151340_019495_metrics.jsonl`.

## Changes and actual validation

- `mj_lab/robots/tita/stand_one_leg_env_cfg.py`: positive two-foot warmup, 2 s delay and nominal/zero-velocity reset.
- `mj_lab/checkpoint.py`: saved reset-on-policy-entry flag for stationary step-in-place tasks.
- `sim2sim/sim2sim_ros2_jazzy/sim2sim_ros2_jazzy/checkpoint.py`: validate/restore the optional flag.
- `sim2sim/sim2sim_ros2_jazzy/sim2sim_ros2_jazzy/sim2sim_node.py`: reset to saved initial state on first policy step when requested.
- `test/test_mjlab_stand_one_leg.py`: warmup reward, reset state, 2 s clock, optional schema and contact-termination regressions.
- `test/check_sim2sim_walk_state_machine.py`: assert initial policy joint pose and use the saved settling time.
- New `test/diagnose_one_leg_startup.py`: frozen-policy and zero-action reset comparison.
- `mj_lab/README.md`, `sim2sim/README.md`: document current warmup/reset behavior.
- Evidence and this report under `docs/exp/2026-10-28/`.

PASS: native task + inline + flat/walk regression: **38 passed, 8 conditional skips**; `one_leg_standing_warmup_tests.log`.

PASS: focused updated schema/reset suite: **8 passed**; `one_leg_standing_schema_tests.log`.

PASS: legacy sim2sim command/gait/action/state-machine unit suites: **18 passed**; `one_leg_standing_legacy_tests.log`.

PASS: two actual ROS/MuJoCo/ONNX protocol cases using the recorded temporary fixture, manual-key callbacks and headless; `one_leg_standing_runtime_checks.json`.

PASS: `./scripts/agent-check.sh`: **720 Python syntax checks**, **8 URDF XML parses**, diff integrity and experiment-directory checks; `one_leg_standing_warmup_agent_check.log`.

PASS: final incremental diff inspected in `one_leg_standing_warmup_changes.diff`; hashes verify unrelated task configs, common MDP, gains and learner entrypoint unchanged. Temporary fixtures removed. Pre-existing work preserved; no commit/push/publication or hardware execution.

Unresolved risks: successful standing/gait learning still requires evaluation of later checkpoints. The diagnosis concerns repeated training-episode resets, not a viewer process closing. Full flat-reward warmup is a pending design discussion and is not the current configuration.
