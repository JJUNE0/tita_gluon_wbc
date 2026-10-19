# sim2sim MOO-checkpoint deployment — handoff index

**Execution domain:** `VALIDATION_SIM` (MuJoCo sim-to-sim only, no hardware touched).
**Scope:** deploying successive RL checkpoints from the `isaaclab_add_reward_autotuning`
repo (task `Tita_Flat_Stand_Drive-v3-mooppo`, co_rl/MOOPPO training framework) into
`tita_gluon_wbc/sim2sim/cosim_ros2_jazzy`, a ROS2 Jazzy + MuJoCo closed-loop harness
originally built only for a different ("DDT-track") obs/action interface.

Read these files in order if you are picking this work up fresh:

1. [`01_checkpoint_history.md`](01_checkpoint_history.md) — every checkpoint deployed
   in this line of work, its config file, and what changed each time.
2. [`02_rma_teacher_architecture.md`](02_rma_teacher_architecture.md) — the RMATeacher
   (Rapid Motor Adaptation) network architecture used by the newest checkpoint
   (`model_9999.pt`, run `2026-08-08_16-12-19`), which is structurally different from
   every prior checkpoint.
3. [`03_code_changes.md`](03_code_changes.md) — exact code added/modified in the
   sim2sim harness to support RMATeacher, file by file.
4. [`04_reference_transform_up_issue.md`](04_reference_transform_up_issue.md) — an
   unresolved, structural stability issue in one FSM state, and why pose/timing
   tuning alone cannot fix it.
5. [`05_validation_and_launch.md`](05_validation_and_launch.md) — exact commands to
   export ONNX, build the ROS2 package, validate headless, and launch the viewer.
6. [`06_open_items_next_steps.md`](06_open_items_next_steps.md) — what is NOT done yet.

## Current state (as of 2026-08-09)

The most recently deployed checkpoint is `model_9999.pt` from run
`2026-08-08_16-12-19` (RMATeacher architecture), config
`sim2sim/cosim_ros2_jazzy/config/tita_moo_stand_drive_20260808_9999_rma_teacher.yaml`.
It is currently running in the MuJoCo viewer (headless smoke-test passed first,
20s, no crash, ONNX shapes verified). Operator (user) is expected to drive it via
`keyboard_command_node` from their own terminal.

## Key repo locations

- Training checkpoints: `/home/cocel/Desktop/Research/isaaclab_add_reward_autotuning/logs/co_rl/Tita_Flat_Stand_Drive-v3-mooppo/mooppo/<run_id>/model_<iter>.pt`
- sim2sim harness source: `tita_gluon_wbc/sim2sim/cosim_ros2_jazzy/cosim_ros2_jazzy/`
- sim2sim configs: `tita_gluon_wbc/sim2sim/cosim_ros2_jazzy/config/tita_moo_stand_drive_*.yaml`
- Exported ONNX artifacts: `tita_gluon_wbc/tita_gluon_ws/deploy/tita/policy_moo_stand_drive_*.onnx`
- ROS2 workspace root actually used for `colcon build`: `tita_gluon_wbc/sim2sim/`
  (NOT `tita_gluon_ws/` — that name is misleading, the colcon `install/`/`build/`/`log/`
  directories live under `sim2sim/`).

## Operating pattern established with the user (Korean-speaking)

- User gives a checkpoint directory path and expects the agent to: inspect
  `agent.yaml`/`env.yaml` for the exact obs/action contract and any architecture
  changes, export ONNX itself via `play.py` (with the correct gym `--task` id —
  wrong task id silently builds the wrong network and fails to load weights),
  create a new descriptively-named config file (never overwrite prior ones —
  additive/reversible history), validate via headless launch before showing the
  viewer, then launch the MuJoCo viewer for the user to drive via the keyboard node.
- User prefers terse "go ahead" instructions once the pattern is established —
  do not re-ask permission for each step of an already-established workflow.
- Do not "fix" `stand_jpos` / FSM tuning values speculatively — the user has
  explicitly set `reference_transform_up.stand_jpos` to
  `[-0.05, 0.9, -2.6, 0.0, 0.05, 0.9, -2.6, 0.0]` (the original ad-hoc pose) and
  it must be carried forward unchanged into new configs unless the user says
  otherwise. See `04_reference_transform_up_issue.md` for why this can't be
  "solved" by pose/timer tuning anyway.
