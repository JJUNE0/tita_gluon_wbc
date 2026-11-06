# TITA mjlab migration and FlashSAC port

Execution Domains: TRAINING_SIM, VALIDATION_SIM, DESKTOP_DRY_RUN

Evidence Status: SUSPICIOUS overall: the implemented pipeline checks PASS;
one pre-existing regression fixture FAIL is retained and explained below.
Walking skill after full training is NOT_TESTED.

Policy Checkpoint SHA256 (latest walk, actor.pt):
`4c440548de8aa939f96b21505e6682550aabdbb58c987e39cc71a3cfbd93d8e3`

Policy Checkpoint SHA256 (final flat, actor.pt):
`71d3dd8577d5b9efd704e65d9a5e98a16c150a816c27eeb5e06a527e30146c62`

Branch: `agent/codex/tita-walk`. No commit, push, PR or hardware operation.

## Changes and preserved work

- Physically moved `lab/` to `isaac_lab/`. The 255 tracked files are staged as
  path-only renames using their original indexed blob IDs. Pre-existing content
  edits remain unstaged. The local ignored `lab -> isaac_lab` symlink supports
  the existing training process and historical absolute paths.
- Added `.gitmodules` and the `third_party/mjlab` gitlink, pinned to official
  v1.6.0, commit `0fb8a681136be94ffc636a3dd423cabb97d91f10`.
  Source: <https://github.com/mujocolab/mjlab>.
- Added `mj_lab/robots/tita/{robot_cfg,flat_env_cfg,walk_env_cfg,mdp}.py`.
  Corrected TITA MJCF/meshes are reused from `sim2sim/robot/tita/mujoco_corrected/`;
  the asset itself was not edited. Wheel collision cylinders are converted to
  spheres in memory, while visual geometry and inertias are preserved.
- Added the mjlab FlashSAC adapter, train/play entry points, checkpoint interchange
  metadata, package installation config and README. Native training is headless;
  video and the existing desktop sim2sim viewer provide inspection.
- Reused the existing FlashSAC config, learner, networks, replay and update code.
  The pre-task SHA256 audit confirms all 17 vendored FlashSAC files are unchanged.
- Shared video orchestration accepts an optional player path; its default remains
  the Isaac player. The sim2sim loader accepts explicit mjlab wheel geometry and
  verifies its saved playback-config hash. These are the only new shared-runtime
  behavior changes beyond source path replacements.
- Updated active path references, root/Isaac documentation, ignore rules and
  agent-check/test-fast coverage. Added `test/test_mjlab_tita.py` and
  `test/check_mjlab_migration.py`. Historical experiment documents were preserved.
- Audited 5,569 pre-task files: none missing, no unexpected modifications, all
  other migration edits are mechanical path replacements. Full local evidence:
  `mjlab_migration_audit.json`, `mjlab_git_rename_audit.json`,
  `mjlab_path_migration.json` and the pre-task snapshot/patch.

The existing Isaac process PID 418996 continued running during migration. Its
native regression checks were rerun successfully after the rename.

## Runtime and behavior

Installed a separate environment at `/home/cocel/venvs/tita_mjlab`:
Python 3.12.3, Torch 2.9.1+cu128, MuJoCo/MuJoCo Warp 3.11.0, Warp 1.18.0,
RTX 3090. Existing Isaac and ROS validation environments were not upgraded.

Data flow: normalized FlashSAC actions → existing piecewise gains → eight native
joint action terms → frozen 0–4 physics-step command delay → PD and torque caps →
MuJoCo Warp → native observations/rewards/terminations → replay. The actor and
critic remain separate: flat 35/39, walk 39/43. Joint observations retain Isaac's
interleaved L1,R1,... order; actions retain L1–4,R1–4 order.

Manual reset mode captures real terminal observations before resetting ended
rows. Non-ended rows keep their original observation noise samples. Timeout
truncation remains distinct from failure termination for value bootstrapping.
Config closures use cloudpickle; actor/critic/optimizer files retain the existing
FlashSAC format. Native config, derived playback contract, source hashes and
mjlab revision are saved with each checkpoint.

Walk retains vx/vy ±0.5 m/s, yaw 0, a 1-second settle and 0.3/s command ramp.
Gait remains active at zero command: period 0.8 s, stance 60%, clearance 4 cm.
Wheel velocity target scales are 0 with wheel PD 0/0.5; this is passive braking,
not a mechanical wheel lock. Base and knee force-history contact >1 N terminate;
failure reward is −10. Hip/roll-rate/pitch-rate weights are −0.1/−0.02/−0.1.
Flat orientation remains −5. Common reward kernels were checked against the
existing Isaac source without starting Isaac in the mjlab process.

W&B online logging and a 500-frame vx/vy overlay video every 10,000 vector steps
remain the training defaults. Metrics, SDK logs, video evidence and TensorBoard
logs are stored under `docs/exp/YYYY-MM-DD/`; weights/configs remain under
`mj_lab/logs/flash_sac/`. Short smoke tests override cadence for quick verification.

## Executed checks

| Domain / check | Evidence status and observed result |
|---|---|
| DESKTOP_DRY_RUN: source migration audit | PASS: 5,569 files preserved; 17 vendor files unchanged; path-only index renames |
| TRAINING_SIM: native mjlab pytest | PASS: 16 passed, 3 inapplicable flat/walk cases skipped; `mjlab_native_tests.log` |
| TRAINING_SIM: Isaac native walk regression | PASS: 73/73 checks; `mjlab_migration_isaac_checks.json` |
| TRAINING_SIM: final flat learner | PASS: 8 envs × 40 vector steps; 35 finite updates; `tita_mjlab_221712_098926` |
| TRAINING_SIM: walk at intended batch size | PASS: 1,024 envs × 12 vector steps; 10 finite updates; `tita_mjlab_221710_985132` |
| TRAINING_SIM: final full-state resume | PASS: 1,024 envs, step 12 → 20; 6 new finite updates; `tita_mjlab_221928_311507`; offline SDK/video log-location check |
| VALIDATION_SIM: W&B video worker | PASS: online 50-frame videos uploaded and SDK sync completed; latest online run below |
| VALIDATION_SIM: native flat video | PASS: 20 frames; `mjlab_flat_preview.json` and MP4 |
| VALIDATION_SIM: ONNX flat/walk exports | PASS: 256 samples each; max error 5.01e−6 / 5.07e−6 for the final physics/config variants |
| VALIDATION_SIM: existing ROS MuJoCo launcher | PASS: walk checkpoint, 100 policy steps, finite state, viewer threads stopped; `mjlab_shared_sim2sim.log` |
| DESKTOP_DRY_RUN: existing focused regressions | FAIL overall: 49 passed, 1 skipped, 19 subtests passed; one pre-existing hip fixture failure |
| DESKTOP_DRY_RUN: `./scripts/agent-check.sh` | PASS; syntax/XML/diff integrity and experiment directories; `mjlab_agent_check.log` |

The native suite covers dimensions and ordering, nominal/randomized gains, frozen
delay, wheel target masking, timeout snapshots, partial reset isolation, actual
base contact, knee force-history threshold, zero-command gait, retained ramp
targets, reward-source parity and portable sim2sim metadata.

Latest online smoke run and uploaded video:
[mjlab_walk_1024_port_validation](https://forge.coreweave.com/wandb/bjy6614-postech/tita_flat_flash_sac/runs/hevs8rft).
Video/render/upload records: `tita_mjlab_221710_985132_videos/`.

Exported walk checkpoint actor SHA256:
`1fe7db81522cd53662d7c84517914dec4991490fd2193ee950fa64e19514abf4`.
Its ONNX SHA256:
`1f9f07e47d953500b0f4dce9492357a4614d92a1d1879fe29531f1abceedc713`.
Final flat ONNX SHA256:
`d522edf645bc884c120c7218270034e94d84bece7f9902d2d888c66ee78f7198`.

## Remaining limits

The existing failure is
`test_flash_sac_action_ranges.py::test_signed_gains_preserve_zero_and_normalized_caller`.
It assumes hip default +0.1 while expecting −0.7 from negative gain 2.8; the
computed value is −0.6. The selected source already uses a zero hip default.
Reversing only this task's path substitutions reproduces the exact pre-task
test SHA256, confirming the stale expectation predates this migration. It was
not changed as part of this task.

Physics are not numerically identical to Isaac/PhysX. MuJoCo uses one sliding
friction coefficient and its own contact damping instead of PhysX's independent
static/dynamic friction and restitution randomization. Flat friction is 0.2–1.6;
walk 0.8–1.2. Fused motors share their frozen command-bus delay. Flat inertia
scaling uses one sampled factor per body to preserve valid principal inertias.
The native settling command preserves its sampled target while emitting zero,
then ramps after settling. These differences are explicit in `mj_lab/README.md`.

The smoke checkpoints establish learning/export/logging plumbing only. A full
100,000-step mjlab locomotion experiment has not been started. The previous
Isaac training remains independent. No hardware deployment was performed.

Commands for full training and playback: [mj_lab/README.md](../../../mj_lab/README.md).
