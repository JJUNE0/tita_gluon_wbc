# Minimal TITA sim2sim code

Execution Domain: DESKTOP_DRY_RUN; native playback checks: VALIDATION_SIM.
Evidence Status: PASS for the checks below. GUI was operator-stopped and its
runtime record is SUSPICIOUS; startup, input handling and clean exit were verified.
Branch: `agent/codex/dev_tita_gluon`. No commit, publication or hardware deployment.

Policy Checkpoint SHA256:

| Policy | SHA256 |
| --- | --- |
| FlashSAC model_15000/actor.pt | f330e86adeb4b5be2ed276fae01063df63e15bc625d8ad0125746263c42e73a2 |
| Plain PPO model_1999.pt | 4ce6a6471b70e2fec58cbf5d85f1403d94c172dec372625e3fdbae0cc51b3ca7 |
| Estimator PPO model_1800.pt | 30b0c28a0d8af084f5455527fc5fb990ff9737e3408962b362dc90cc1e8721ba |

## Changes

- Added `sim2sim/AGENTS.md`: preserve the minimum-code policy, one source for
  policy settings, clear control flow, and required validation/evidence.
- Updated `sim2sim/sim2sim_ros2_jazzy/sim2sim_ros2_jazzy/`:
  `adapter.py`, `checkpoint.py`, `cli.py`, `mujoco_env.py`, `sim2sim_node.py`,
  `real2sim_node.py`; removed `keyboard.py`.
- Reduced `config/tita.yaml` from 35 to 13 lines. It contains the MuJoCo scene,
  read-only mirror pose, control timing and interactive command caps.
  Policy dimensions, joint order, scale, offset and PD settings come from
  the saved checkpoint configuration.
- Updated shared `lab/ddt_lab/scripts/flash_sac/export.py`, the two READMEs,
  `test/test_flash_sac_export.py` and `test/test_sim2sim_checkpoint_adapter.py`.

Core execution modules decreased from seven to six; core Python lines decreased
from 934 to 857. Readable formatting and focused observation/action/model
functions take precedence over compressing individual statements.

Removed unused history methods, duplicate default observation/action layouts,
the action debug container, unused MuJoCo reset/accelerometer helpers, duplicate
ONNX Runtime validation, automatic newest-run/step lookup, the state debug
publisher, and the separate keyboard worker/executor management.
Keyboard input and ROS callbacks share one executor. Input waits until the
next control timer deadline, preserving the control period. Viewer render
thread shutdown is retained because it prevents native teardown faults.

Action flow is explicit: signed FlashSAC gains in the actor, then saved
scale -> offset -> processed clipping -> native joint order -> PD -> torque limits.
`ActionAdapter.targets()` exposes joint targets; `compute()` returns torque.
The last-action observation keeps policy order. PPO architecture is restored
from its saved agent configuration, with normalization and optional estimator.
Export verification compares native policy and ONNX through one shared path.

`--ckpt` is now required. `--run`, `--step`, and implicit newest-checkpoint
selection were intentionally removed. The two launch files remain unchanged.
Other training/hardware sources and shared URDF assets were preserved.
The URDF folders are referenced by other lab assets and tests and cannot be
removed as unused simulation code.

## Observed metrics / behavior / log summary

- PASS: 41 FlashSAC CPU regression tests (`sim2sim_minimal_flash_tests.log`).
- PASS: 13 adapter/cache/CLI and native PPO tests
  (`sim2sim_minimal_policy_tests.log`). Plain and estimator PPO outputs match
  native RSL-RL exactly on 512 observations: maximum difference 0.0.
- PASS: two synthetic real2sim tests (`sim2sim_minimal_readonly_tests.log`),
  using localhost domain 87, with no robot command publisher or physical robot.
- PASS: all three policies exported and replayed for 100 MuJoCo control steps
  (`sim2sim_minimal_{flash,ppo,estimator}_runtime.log`). ONNX hashes are identical
  to their pre-minimization exports. Maximum final-position differences versus
  the previous implementation: FlashSAC 1.8626e-7 m, PPO 2.9802e-8 m,
  estimator PPO 2.2352e-8 m. Automated comparison: `sim2sim_minimal_equivalence.json`.
- PASS: installed ROS sim2sim launch, explicit ckpt, 10 steps and child exit 0
  (`sim2sim_minimal_roslaunch.log`).
- GUI: 1016 policy steps, reset/w keys and Ctrl-C, exit 0, viewer threads stopped
  (`sim2sim_minimal_gui.log`). SUSPICIOUS operator stop; no quality claim.

Required final gate: `./scripts/agent-check.sh`, recorded in
`sim2sim_minimal_agent_check.log`. Task-relative diff was inspected against
the before-task archive: `sim2sim_minimal_task_relative.diff`.
Source-integrity comparison found no unexpected changes outside this task.

Before-task snapshot: `sim2sim_minimal_before.tar.gz`, SHA256
`04b77ae784d64240a93abf5be0e026764ab4a137b900d36d446dcc38f4a8450d`.
Checkpoint sidecars remain required. Tests validate mapping and finite playback;
long-horizon quality and real hardware behavior remain NOT_TESTED in this task.
MuJoCo continues to use the clean PD model without training delay/bias randomization.

From the repository root (`VALIDATION_SIM`):

```bash
python3 sim2sim/sim2sim_ros2_jazzy/launch/sim2sim.launch.py --ckpt /path/to/trained.pt
```
