# Zero-command single-leg standing: minimal reward environment

Execution Domains: TRAINING_SIM (environment/native CUDA tests), DESKTOP_DRY_RUN (operator pose capture and repository checks).

Evidence Status: PASS for configuration, reward arithmetic, native finite rollouts, serialization and saved gait contract. Learned single-leg balance, policy export with trained weights, and full training are NOT_TESTED. No new learning run was started.

Policy Checkpoint SHA256: N/A — code-only task; no policy checkpoint was created.

Branch: `agent/codex/tita-walk`.

## Operator intent and pose reference

The user confirmed that the support axis means the hip-center to wheel-center line and allowed substantial body tilt. The demonstrated RViz pose is a qualitative reference; it is not an exact joint-angle target. Snapshot: `stand_one_leg_operator_reference.json`; image: `stand_one_leg_operator_reference.png`.

Captured body roll is approximately 32 degrees. The left hip-to-wheel line is approximately 10 degrees from world vertical, while the opposite leg is folded/angled. The snapshot is kinematic, with both wheel bottoms around 4 cm above the grid; it is not a measurement of physical ground support or balance. No recorded joint angle or body tilt is loaded into the reward.

## New task and preserved MDP components

Added `mj_lab/robots/tita/stand_one_leg_env_cfg.py`, class `TitaStandOneLegEnvCfg`, factory `make_stand_one_leg_env_cfg`, and FlashSAC task name `stand_one_leg`.

The task inherits inline's observations/actions, active wheel policy, PD, torque limits, delay/gain/knee randomization, full domain randomization, contact sensors and base/knee/time-out terminations. Shared `mdp.py`, existing flat/walk/inline configs, robot parameters and checkpoint/player code were unchanged; hashes are recorded in `stand_one_leg_env_preserved_hashes.json`.

Velocity commands vx/vy/yaw are always zero. The fixed straight-command cohort is disabled. Gait runs after its existing 1 s settling window even at zero command. Frequency is 0.5 Hz (2 s full cycle), stance fraction 0.75, left/right offset 1 s and nominal swing window 0.5 s per foot. Float32 phase threshold sampling can move a boundary by one 20 ms control tick; the tests check this discretization explicitly. Double support fills the remaining phase intervals; no flight phase is requested.

Actor/critic/action dimensions remain 40/44/8. The native checkpoint contract and sim2sim observation builder preserve the zero-command stepping mode.

## Exactly five reward terms

| Term | Manager weight | Behavior |
| --- | ---: | --- |
| `gait_support` | +2 | Correct scheduled contacts earn swing-clearance credit; wrong contacts subtract from the same term. No body-upright multiplier. |
| `support_leg_tilt` | -1 | Single-support hip-to-wheel axis cost `1 - cos(tilt)` in world coordinates. |
| `stationary` | -0.5 | World planar base velocity squared plus `0.1 * world yaw angular velocity squared`. |
| `action_rate` | -0.005 | Existing native action-change squared penalty. |
| `termination` | -10 | Existing non-timeout termination indicator. |

Let `d_i` be desired stance contact from gait, `c_i = (norm(force_i) > 5 N)`, and `e = sum_i (c_i != d_i)`. For a desired swing foot, clearance credit is `clip(h_i / 0.04, 0, 1)`; desired stance feet contribute a factor of one. Their product is `H`. The combined gait term before timestep scaling is:

`2 * gait_enabled * (all_contacts_correct * H - e)`.

Consequently, a grounded swing foot costs -2, a missing stance-foot contact costs -2, swapping the support foot costs -4, and correct support with 4 cm swing clearance earns +2. Half clearance earns +1. Contact errors during double support are also penalized. All these are weighted reward values before the reward manager's timestep scaling. The contact check uses force magnitude, independent of the mjlab wrench sign.

The 4 cm value is a soft clearance target, not a hard maximum: extra lift earns no additional credit. It is held as the target during the requested swing window; there is no exact pose trajectory or forced instantaneous joint motion. Positive contact/height credit requires the correct support foot; missing support is explicitly penalized.

The support axis is `*_leg_2` (hip pitch pivot) to `*_leg_4` (wheel center), checked only during requested single support. Body orientation itself, roll/pitch angular rates, joint deviations and base height have no reward terms. No fixed world-position or separate COM target is imposed. The body and opposite leg are free to redistribute mass while the dynamics and contact objectives determine balance.

## Validation actually executed

PASS: `/home/cocel/venvs/tita_mjlab/bin/python -m pytest test/test_mjlab_stand_one_leg.py test/test_mjlab_inline.py test/test_mjlab_tita.py -q`: **35 passed, 8 conditional skips**, 3 existing mass-randomization warnings; `stand_one_leg_env_tests.log`.

Coverage includes grounded swing-foot penalty, missing/wrong support penalty, double support, partial clearance, force sign, world-origin invariance, support-axis geometry, swing-leg freedom, body-tilt independence, zero commands, 0.5 s swing timing, native finite CUDA rollouts, environment cloudpickle roundtrip and zero-command gait restoration in the sim2sim builder.

Intermediate logs are retained. Test development first exposed an inclusive floating-point tolerance edge at one control tick and a missing `policy_interface` field in the test's partially prepared playback config. Both test fixtures were corrected; no shared gait/runtime behavior was changed to satisfy them.

PASS: `/home/cocel/venvs/tita_mjlab/bin/python -m mj_lab.scripts.train --help`: normal CLI import/help exit, without constructing a training run; `stand_one_leg_cli_help.log`.

Actual operator pose and namespaced TF were captured through read-only subscribers on ROS domain 88. The initial TF probe used the wrong absolute topic names; the successful probe remapped both TF topics to `/tita_pose_preview/`. The preview remains running.

Repository agent-check results are in `stand_one_leg_env_agent_check.log`.

## Changes and operational state

- New `mj_lab/robots/tita/stand_one_leg_env_cfg.py`: standalone task and its three task-specific kernels; shared MDP functions are reused without changing them.
- `mj_lab/scripts/train.py`: register `--task stand_one_leg`; the default remains inline.
- `mj_lab/README.md`: document the task, five rewards and manual future launch command.
- New `test/test_mjlab_stand_one_leg.py`: five focused tests, including native physics checks.
- Pose, logs, provenance and this report under `docs/exp/2026-10-28/`.

Incremental diff: `stand_one_leg_env_changes.diff`. Pre-existing changes were preserved and no unrelated source files were edited. No commit, push or publication was performed. The existing inline training process was not stopped, restarted or reconfigured; this task adds no automatic training queue.

When explicitly starting a future experiment, use the dedicated mjlab interpreter and omit resume/warm-start. The command is documented in `mj_lab/README.md`; it was not executed here.

Unresolved risks: these are initial reward coefficients, not validated learning results. Large body tilt is permitted until physical base/knee ground contact triggers termination. No claim is made that the static reference pose is dynamically feasible. No hardware execution was performed.
