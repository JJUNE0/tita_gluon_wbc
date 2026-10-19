# Sim2sim command range from checkpoint

Execution Domain: VALIDATION_SIM / DESKTOP_DRY_RUN

Evidence Status: SUSPICIOUS overall: focused verification PASS; required agent-check FAIL on unchanged pre-existing trailing whitespace.

Policy Checkpoint SHA256: `9c22f34e0e3b9d7840f29250c214452bb84cadde6037d277d90df55221e84150`

ONNX SHA256: `128734f230868b947c9eac59ef647b8394043c6603781a335fd4e3b4700a2001`

Branch: `agent/codex/dev_tita_gluon`

Changed files:
- `sim2sim/sim2sim_ros2_jazzy/sim2sim_ros2_jazzy/checkpoint.py`
- `sim2sim/sim2sim_ros2_jazzy/sim2sim_ros2_jazzy/sim2sim_node.py`
- `sim2sim/README.md`

Behavior: the shared exporter saves sim-only `sim_command_ranges` from training's base_velocity ranges. PosKneeMA2 now permits [-1, 1] m/s forward/backward and [-1.5, 1.5] rad/s yaw, previously +/-0.2 and +/-0.3. Keyboard and ROS commands use the same bounds, including asymmetric ranges if saved that way. Keyboard acceleration ramp 0.5 and inactivity timeout 0.5 s remain. Robot caps in the existing command section are unchanged; no sim2real source, robot bundle or deployment changed. Older prebuilt configs retain their old caps until regenerated; normal checkpoint launch automatically invalidates the old cache and reexports.

Executed checks:
- PASS `prepare.log`: public --prepare-only path rebuilt model_75000 cache; native/ONNX parity over 256 inputs, max error 3.4571e-6.
- PASS `verification.log`: real ROS/MuJoCo node accepts positive/negative full ranges and intermediate 0.7 m/s + 0.9 rad/s commands; clips +/-20 commands at saved bounds. Original robot command caps verified as 0.2 m/s / 0.3 rad/s.
- PASS: 250 finite MuJoCo steps, including 100 RL steps with vx=0.7 m/s and yaw=0.9 rad/s. This verifies execution/input handling, not tracking quality or high-speed stability.
- PASS: task-specific diff whitespace checks and tracked-file integrity; unrelated tracked changes: none. Pre-existing edits snapshotted before modification.

Use the normal sim2sim checkpoint command after restarting the current viewer. No new runtime flag is required. No hardware commands, robot deployment, commit or publication performed.

Required `./scripts/agent-check.sh` executed: FAIL solely from six pre-existing trailing-whitespace lines in `my_flat_env_cfg.py` (431, 437, 443, 449, 455, 461); task-start/current hashes match. Python syntax: 635 PASS, 0 FAIL; URDF parsing: 8 PASS; experiment directories PASS. Final task diff reviewed; only the three listed source/doc files changed beyond the scoped generated export and evidence. No unrelated tracked changes.
