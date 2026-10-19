# Minimal sensor-reward MuJoCo FlashSAC fine-tuning

Execution Domain: VALIDATION_SIM (integration), DESKTOP_DRY_RUN (unit checks)

Policy Checkpoint SHA256 (source actor.pt): `6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05`

Evidence Status: SUSPICIOUS — functional checks pass; the initial candidate regresses against the source policy.

## Implementation and use

New entry: `sim2sim/sim2sim_ros2_jazzy/launch/sim2sim_finetune.py`.
It runs directly with Python, without ROS or the playback state machine.
The existing playback files and all pre-existing repository changes are untouched.
This file is a source-tree entry point; the existing setup.py only installs `*.launch.py` files.

The interpreter needs PyTorch, gymnasium, MuJoCo, NumPy and PyYAML together.
The installed Isaac interpreter is Python 3.11 and has Torch/gymnasium but no MuJoCo;
the playback interpreter is Python 3.12 and has MuJoCo but no Torch/gymnasium.
For validation only, MuJoCo 3.3.7 and its missing dependencies were installed in
`/tmp/tita_finetune_deps`, without changing either existing environment.

```bash
PYTHONPATH=/tmp/tita_finetune_deps \
  ~/isaac/env_isaaclab/bin/python \
  sim2sim/sim2sim_ros2_jazzy/launch/sim2sim_finetune.py \
  --steps 10000 --min_buffer 256 --batch_size 64
```

The default checkpoint is the requested `tita_flash_sac_115632_883848/model_60000`.
`--ckpt MODEL_DIRECTORY` chooses another compatible FlashSAC actor.
`--vx 0.1 --yaw_rate 0.1` selects a fixed command, within the existing sim2sim limits.
Zero command is the default. `--viewer` opens MuJoCo; otherwise the run is headless.
`--eval --steps 1000 --ckpt MODEL_DIRECTORY` evaluates deterministically without
updates or saving network weights. Commands, seed and episode length should match
between baseline and candidate evaluation. Viewer mode does not impose wall-clock pacing.

Defaults: 1 environment, 50 Hz control from the checkpoint, replay capacity 50,000,
minimum 256 transitions, batch 64, 1-step returns, one learner update per new transition,
256 critic-only updates before normal FlashSAC updates, learning rate 1e-5,
exploration scale 0.1 using the existing temporally repeated FlashSAC noise.
The first critic update is at transition 256; the first actor update is at transition 512.
`--min_buffer 64 --batch_size 32` or even `--min_buffer 1` is mechanically allowed;
small correlated buffers and sampling with replacement do not establish learning reliability.
These are initial engineering defaults, not values established for this robot by a paper.

Every invocation loads only actor weights and starts critics, temperature, reward
statistics, optimizers, and replay fresh. This deliberately changes the objective,
dynamics domain and critic velocity source; the saved Isaac critic does not estimate
the new return. Re-running with an output checkpoint is another actor warm start,
not exact training resume. Critic warmup freezes actor and temperature.

## Reward and data semantics

The shared `sensor_reward` function accepts only calibrated body-frame IMU orientation,
gyro, native-order joint positions/velocities, command, normalized current/previous
actions, wheel radius and control dt. No ground-truth position/velocity, contact force,
motor-current measurement, or privileged simulator signal is required by the reward.

For speed proxy v, body yaw gyro wz, projected gravity g and normalized action a:

```text
r = dt * [2 exp(-((v - vx_cmd)/0.25)^2)
          + exp(-((wz - wz_cmd)/0.5)^2)
          - 5 (gx^2 + gy^2)
          - 0.05 (wx^2 + wy^2)
          - 0.01 sum((a - a_prev)^2)]
    - 1 if tilted more than 60 degrees from upright
```

The final fall penalty is an event penalty, outside dt scaling.
The speed proxy uses the known TITA joint axes, hip positions, shoulder/knee/wheel
encoder rates and IMU pitch rate to estimate rolling motion at the wheel axle.
Wheel radius is read from the model collision cylinders (0.0925 m).
It assumes no slip, uses nominal URDF axis geometry, and is not base-link ground-truth
speed. Leg motion/geometry, wheel slip and airborne spinning can bias or exploit it.
Actual world drift cannot be established from this reward alone. Ground-truth base
forward velocity is logged only as a simulation diagnostic and never fed to learning.

Actor observations retain the checkpoint's 33-dimensional layout. Critic observations
retain its 36-dimensional layout with body linear velocity replaced by `[v_proxy, 0, 0]`.
All observation scales, joint order, PD settings, action gains and native action terms
come from saved checkpoint sidecars. Replay stores normalized [-1, 1] actions, while
the simulator receives the saved piecewise gains and observation last_action stores
those applied actions, matching the original training wrapper.

Tilt terminates an episode; elapsed episode time truncates it. Replay receives the
pre-reset next observation even for timeouts, so only genuine terminations suppress
bootstrapping. Sim episodes automatically reset directly to the checkpoint pose.
Real robots require a separately approved operator/reset and control implementation;
automatic MuJoCo resets are not a hardware recovery procedure.
The present loop runs physics and gradient updates synchronously; a real controller
must maintain its control deadline independently of learning and checkpoint writes.

All run metrics, weights, replay and summaries go under `docs/exp/YYYY-MM-DD/`.
Saved model directories retain actor export compatibility. No `env.pkl` is copied:
the Isaac training `--resume` path must not silently restore the original reward.
Saved replay is available for later prior-data experiments; this implementation does
not load or mix an offline dataset and does not implement RLPD or Cal-QL.

## Research basis

- [FlashSAC](https://arxiv.org/abs/2604.04539): existing off-policy learner and update
  kernels are reused. Its high-throughput simulation results do not validate a tiny
  single-robot replay buffer.
- [RLPD: Efficient Online Reinforcement Learning with Offline Data](https://arxiv.org/html/2302.02948v3):
  supports off-policy online RL with prior trajectories, using 50/50 prior/online
  sampling, critic normalization and other design choices. It explicitly reports
  that naive SAC plus prior data is insufficient in its benchmarks. Current source
  checkpoint has no saved replay, so there is no offline dataset to mix here.
- [Cal-QL](https://arxiv.org/abs/2303.05479): highlights the importance of value
  initialization/calibration for offline-to-online transfer. This runner resets the
  old critic because the reward and observation source changed; it does not claim
  to implement calibrated Q-learning.

If prior simulation/real trajectories are later reused with this reward, store the
necessary raw sensor/command/action information and recompute rewards consistently.
Equal reward formulas do not make simulator transitions samples of real dynamics.

## Observed metrics / behavior / log summary

- `sim2sim_finetune_tests.log`: PASS, 7 tests, including real MuJoCo steps and actual
  FlashSAC gradient updates; exact actor loading; actor unchanged during critic warmup;
  actor changes on subsequent joint updates; normalized replay action vs applied action;
  timeout terminal snapshot and bootstrapping mask; tilt termination; independence
  from simulator translation and root linear velocity.
- Initial 32-transition integration: PASS, 25 updates, 11 actor updates, 3 timeouts,
  no falls, saved weights and replay; source checkpoint unchanged.
- Default-setting 1,200-transition integration: PASS for execution, 945 total learner
  updates (256 critic-only, 689 normal FlashSAC updates including 345 actor updates),
  no falls, 2 timeouts. Weights and replay saved at
  `sim2sim_finetune_224941_966220/model_1200`.
- `sim2sim_finetune_export.log`: PASS, existing export path accepts the new checkpoint;
  256 PyTorch/ONNX parity samples, max absolute action error `5.126e-6`.
- Paired deterministic evaluation: 1,000 steps each, same seed 42, zero command,
  10-second episodes, no exploration and no learning. Both completed without falls
  and with 2 timeouts. Evaluation quality is SUSPICIOUS:

| Metric | Source model_60000 | Fine-tuned model_1200 |
| --- | ---: | ---: |
| Mean reward / step | 0.058484 | 0.018458 |
| Rolling speed proxy RMSE (m/s) | 0.054458 | 0.801498 |
| Diagnostic true base forward speed RMSE (m/s) | 0.020963 | 0.128474 |

The initial candidate is worse. Do not treat its successful updates/export as evidence
of better control. Tiny-buffer off-policy updates plus short critic warmup are not
sufficient to preserve the source behavior in this experiment. The runner is an
experimental fine-tuning path, not a validated tuning recipe. Longer critic fitting,
actor constraints/prior data, and multiple-seed paired evaluation are subsequent
experiments, rather than claims established by this implementation.

Run logs: `sim2sim_finetune_training_smoke.log`, `sim2sim_finetune_baseline.log`,
`sim2sim_finetune_candidate_eval.log`; the individual run summary files retain all
arguments, source/output hashes, implementation hash and results.
The initial 32-transition check used reduced buffer/batch/episode settings and is
only a mechanics check. Source actor hash was rechecked and remains unchanged.

Repository completion check output: `sim2sim_finetune_agent_check.log` (the log's
final result records the actual status, including any pre-existing repository errors).
Task changes are additive: the launcher, `test/test_sim2sim_finetune.py`, and these
experiment reports/logs/artifacts. Existing playback/training/hardware sources were
not edited. The task diff was reviewed using `git diff --no-index /dev/null FILE`
because the new entry point and test are untracked in the existing worktree.

Hardware execution: NOT_TESTED. No robot command, hardware connection or deployment.
Long-run/multiple-seed policy improvement: NOT_TESTED.

Branch: `agent/codex/dev_tita_gluon`. No commit, push or PR requested.
