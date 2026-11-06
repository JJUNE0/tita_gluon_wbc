# Support-mode sim2sim and state-machine confirmation

Execution Domains: VALIDATION_SIM, DESKTOP_DRY_RUN.

Evidence Status: PASS for export, state-machine startup, support-command delivery and switches without reset. NOT_TESTED for sustained balance quality during mode transitions.

Policy checkpoint: `mj_lab/logs/flash_sac/tita_mjlab_163835_917365/model_25000`.

Policy Checkpoint SHA256: `436ff2b3c2752a67e618c53a7c83c9b8e2415aee3437ea5ccb525999c674daf7`.

ONNX Hash: `c490ba59c76652fd0170f170e92e06ebfd6656bf297f335863e75920f787ad4f`.

Branch: `agent/codex/tita-walk`.

The existing implementation was inspected and reused without modifying production source. A fresh export and actual ROS/MuJoCo/ONNX verification were performed against the full experiment's 25,000-step checkpoint, replacing the earlier pipeline-probe evidence for this confirmation. Training was not stopped or changed.

## State and command flow

- Existing state machine: `idle` at SPLAY -> `transform_up` -> `sit` -> `rl`. Interactive controls remain `1` to transform and `0` to request policy after reaching sit; `6` selects idle and `2` resets to SPLAY/idle.
- The saved `sim_reset_on_policy_entry=true` initializes physics to the training checkpoint's nominal standing pose once at RL entry, clearing action/filter/observation histories. This is simulation initialization; it does not establish learned sit-to-stand behavior.
- In RL, a discrete support command is passed to the policy as three one-hot inputs: 0 left support/right lift, 1 right support/left lift, 2 both grounded.
- Keyboard `7/8/9` or existing simulated key messages `support_left/support_right/support_both` select IDs 0/1/2. Changing this goal preserves RL state, simulation time and physics. These goals are policy inputs within RL, not additional hand-authored joint trajectories in the startup state machine.
- The CLI supports `--support-mode 0/1/2`; default is both support from the saved contract. Headless mode performs startup automatically. No gait clock or automatic support alternation is used in sim2sim.

## Actual checks

- PASS: latest checkpoint hash verification and actual ONNX export: 38 observations, 8 actions, 256 samples, maximum absolute parity error **4.17e-6**. Log: `support_command_sim2sim_25000_prepare.log`.
- PASS: two actual runtime cases using `test/check_sim2sim_walk_state_machine.py`: manual-key callbacks with passive GUI creation suppressed, and headless automatic startup. Checks include early RL rejection, policy calls only after sit/RL transition, first policy observation at saved nominal joint pose, all three requested one-hot goals, switches without simulation reset, idle/reentry and reset behavior. Local ROS domain 90; no hardware. Results: `support_command_sim2sim_25000_runtime.{json,md,log}`.
- PASS: full CLI with `--headless --steps 140 --support-mode 2`, confirming forwarded mode 2 and finite physics: `support_command_sim2sim_25000_cli.log`.
- PASS: before/after hashes confirm sim2sim production files were not changed during this follow-up: `support_command_sim2sim_followup_sources.json`.
- Required repository checks: `support_command_sim2sim_followup_agent_check.log`.

Changed artifacts this turn are this report, verification logs/JSON, and the generated policy export/cache beside `model_25000`; no source or test script was changed. Existing pre-task work was preserved. Successful command delivery and finite short playback do not establish stable learned single-leg transfers. No physical robot command, deployment or publication was performed.
