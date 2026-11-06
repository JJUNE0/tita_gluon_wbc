# Episode-fixed 40/40/20 support goals and flat rewards for double support

Execution Domains: TRAINING_SIM, VALIDATION_SIM, DESKTOP_DRY_RUN.

Evidence Status: PASS for command persistence/distribution, mode-specific rewards, state isolation, finite learner updates, export, video and sim2sim plumbing. Learned sustained support and physical transition quality remain NOT_TESTED for the new run.

Policy Checkpoint SHA256: full experiment's first checkpoint was pending at startup verification. Separate pipeline-probe actor: `b8f14f1c3bfa7832e2161535f52be595e803d567ae7faac39917de79a990fae7`.

Branch: `agent/codex/tita-walk`.

## Requested behavior

The previous support task sampled a new mode every 3–5 seconds within an episode. Its default single-environment video also overrode goals with a separate 2.5-second 2 -> 0 -> 2 -> 1 demonstration sequence. Both mechanisms can contribute to the visible foot-lowering/raising pattern; this observation alone does not establish that a policy cannot sustain a fixed support goal.

New episodes select one support command and hold it until reset:

| Mode | Episode probability | Goal | Reward set |
| --- | ---: | --- | --- |
| 0 | 40% | Left wheel supports, right lifts | Existing reference-balance rewards, 8 terms |
| 1 | 40% | Right wheel supports, left lifts | Mirrored reference-balance rewards, 8 terms |
| 2 | 20% | Both wheels support | All 18 flat rewards, original coefficients |

These are per-episode sampling probabilities, not guaranteed fractions of physics frames. Different episode lengths can produce different frame proportions. A seeded 20,000-episode assignment test produced **8057 left / 7916 right / 4027 both**. A goal stayed unchanged for 25 simulated command seconds, including an explicitly expired-timer test. Partial reset changes only the reset rows. There is no gait, settling clock, or automatic within-episode goal change.

vx/vy/yaw remain zero. Actor/critic/action dimensions remain 38/42/8. PD, action scales, physical randomization, nominal standing/zero-velocity reset, base/knee contact termination, and the FlashSAC learner are preserved.

New fixed-episode videos use the sampled episode goal rather than the old timed demonstration; the support label now includes episode age. In a complete 500-frame untrained pipeline video, every observed goal change occurred at an episode boundary (`episode_step=0`), never inside an episode. Falls/resets remain visible rather than being hidden. Explicit player/sim2sim support commands still allow operator-selected modes. Saved old timed configs retain their original behavior through default `episode_fixed=False` fields.

## Flat mode and reward isolation

Mode 2 copies the live `TitaFlatEnvCfg(...).rewards` dictionary's functions, parameters and coefficients rather than duplicating a handwritten list. Its terms are:

- Linear tracking +2 / +0.5 / +0.5; yaw tracking +1.
- Vertical linear velocity -2; horizontal angular velocity -0.05.
- Joint torque -1e-5; joint acceleration -2.5e-7; action changes -0.01.
- Joint mirror -1; undesired knee contacts -1; flat orientation -5; base height -10.
- Hip deviation -1; shoulder deviation -0.5.
- Zero-command position drift +1; wheel action -0.05; heading drift +1.

Mode-0/1 weights remain alive +2, contact/clearance +2, pose hint +0.5, support-leg tilt -1, stationary -0.5, action changes -0.005, joint acceleration -2.5e-7 and termination -10. These match the referenced fixed-left `model_40000`; the requested support side is selected symmetrically. All weights retain timestep scaling at 0.02 s.

Manager keys use `one_leg_` and `flat_` prefixes. A row receives only its selected reward set. Mode 2 does not also receive the single-leg alive, pose, contact or termination reward. Its common failure termination conditions remain active. Common observation/reset/velocity-latch settings are retained from the balance task; this is equality of flat reward terms/coefficients, not a claim that the entire original flat environment, moving commands or randomized reset ranges are identical.

Flat position/heading anchors and wheel-action integrals carry internal state. The wrapper restores inactive rows after evaluating those kernels so flat reward evaluation cannot alter single-leg critic observations or accumulate a flat wheel penalty in single-leg rows. Native mixed-mode tests compare every flat term with its direct original kernel and verify both active-row equivalence and inactive-buffer preservation. Rewards are neither double-counted nor applied across the other mode's mask.

`support_episode_reference_comparison.json` records the reference weights, exact flat coefficients, common action/physics/event/termination equality and sampling evidence. The preserved reference checkpoint is `mj_lab/logs/flash_sac/tita_mjlab_155513_268911/model_40000`, SHA256 `fe8ca785da4353b79ef0b5af37ca073495b2156fa72395d939c3171bef8d27dd`. Its actor file was not changed.

## Experiment replacement

After validation, timed-mode run `tita_mjlab_163835_917365` was stopped by user-authorized SIGINT at **48,873 steps / 97,547 updates**. Last complete checkpoint: `model_45000`, SHA256 `59c800edbe0fbf4d1c33437094b4bc522215d1e11a9ecd4ecc38b03e54293eac`. Its generic FAIL/KeyboardInterrupt result denotes the deliberate replacement, not a numerical failure. See `support_episode_previous_stop.json` for the verified process exit and preserved paths.

New run: **`tita_mjlab_173314_948748`**.

W&B: https://forge.coreweave.com/wandb/bjy6614-postech/tita_flat_flash_sac/runs/flgfsisr

PID `1449786`; tmux `mjlab_support_episode442_20261028_173311`.

Initialization: **FROM SCRATCH**; `resume=null`, `warm_start=null`, new W&B run, new networks/optimizers/normalization/replay. Budget: 100,000 vector steps, 1024 environments, seed 42, CUDA 0, two learner updates per step after replay warmup. W&B online, checkpoints every 5,000 steps, 500-frame videos every 10,000 steps.

Startup snapshot: **1,000 steps, 1,802 finite updates**. Learned performance is not claimed from startup. Provenance and source hashes: `support_episode_training_launch.json`; console: `support_episode_training_console.log`; metrics: `tita_mjlab_173314_948748_metrics.jsonl`.

## Files and actual verification

Changed files:

- `mj_lab/robots/tita/support_command_env_cfg.py`: episode-fixed sampler with 40/40/20 probabilities; backward-compatible timed defaults; mode-specific reference/flat reward sets with isolated stateful buffers.
- `mj_lab/checkpoint.py`: save episode-fixed/probability metadata.
- `mj_lab/scripts/play.py`: disable timed demonstration for episode-fixed configs and display goal plus episode age.
- `mj_lab/README.md`: document episode semantics and conditional reward sets.
- `test/test_mjlab_support_command.py`: distribution/persistence/legacy checks, flat-kernel equivalence and state isolation.
- Evidence and this report under `docs/exp/2026-10-28/`.

Executed results:

- PASS: scoped native/reference/old-alternating/inline/flat-walk/sim2sim suite: **67 passed, 8 conditional skips, 39 subtests passed**, `support_episode_tests.log`.
- PASS: fresh 16-environment, 40-step learner probe: **74 finite updates**, checkpoint save and pickle reload; `support_episode_learner_probe.log`, `tita_mjlab_172855_759993/model_40`.
- PASS: 500-frame video encode/decode and audit that goals change only at episode boundaries; `support_episode_video_probe.json`, `support_episode_video_decode.json`, `.mp4`.
- PASS: actual 38-input/8-action ONNX export, 256-sample max absolute parity error **5.25e-6**, `support_episode_sim2sim_prepare.log`.
- PASS: two actual local ROS/MuJoCo/ONNX startup and manual-command cases with all three support IDs, no reset on mode selection; `support_episode_sim2sim_runtime.{json,md,log}`. These verify command plumbing, not trained transition stability. No sim2sim runtime source was changed in this task.
- PASS: active sources match launch and unrelated training sources/reference actor are preserved; `support_episode_source_verification.json`.
- Required repository checks and final incremental diff: `support_episode_agent_check.log`, `support_episode_changes.diff`.

Risks/limits: holding a goal removes command-driven switching but does not by itself prevent physical touchdown/lift oscillations. Existing support-time metrics are cumulative, not longest continuous holds. This stage trains sustained support from reset; stable left/right transfers still need later evaluation/curriculum. No new lift-height cap was added. No hardware control, deployment, commit or publication was performed.
