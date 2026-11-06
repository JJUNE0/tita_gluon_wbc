# Support-velocity playback and continuous RL entry

- Execution Domains: VALIDATION_SIM and DESKTOP_DRY_RUN.
- Evidence Status: PASS for interface flow, no-reset entry, tilt protection and scoped checks; SUSPICIOUS for learned transition/tracking quality described below.
- Branch: `agent/codex/tita-walk`.
- Checkpoint: `mj_lab/logs/flash_sac/tita_mjlab_194029_719452/model_15000/actor.pt`.
- Policy Checkpoint SHA256: `cb631c7e55b25113f99560dbc35067630afef68a1e2235827d95bfc98ca6af21`.
- ONNX SHA256: `c36c67576dc201862e3f5fe80ddade3e3de7f89c7e062a1112df8acf83c0a3d1`.

## Resulting behavior

The new support-velocity task already exported vx/yaw ranges of +/-0.5 m/s and +/-0.5 rad/s, disabled vy, and the same three one-hot support inputs. The normal checkpoint launcher now prepares the actual 15k training checkpoint. The existing keyboard supports `w/s` vx, `a/d` yaw, `r` stop and `7/8/9` left/right/both support; startup remains `1` prepare and `0` RL.

The user reported the robot appearing to respawn after `1` then `0`. The cause was the runtime's `sim_reset_on_policy_entry` branch calling `env.reset()` to force a nominal standing state. That branch is removed. The existing stable SPLAY-to-SIT preparation remains unchanged; RL starts from its actual qpos, qvel and simulation time. Legacy reset-hint metadata is ignored, and explicit keyboard `2` / ROS reset requests retain their intentional reset behavior. Observation/action histories still reset appropriately on entering/exiting policy control.

Support-policy RL also now applies `control.support_fall_tilt_deg: 55.0` from `sim2sim/sim2sim_ros2_jazzy/config/tita.yaml`. Above that total tilt, the policy is no longer evaluated, target/emitted commands and actions are cleared, and the state machine applies only velocity damping clipped to the existing joint effort limits. Direct RL entry from damping is rejected; preparation is required again. The tilt fault does not respawn physics. Reports record fault count and final state. The user's existing ground friction 0.2 was preserved.

## Changed files

- `sim2sim/sim2sim_ros2_jazzy/config/tita.yaml`: support RL tilt setting.
- `sim2sim/sim2sim_ros2_jazzy/sim2sim_ros2_jazzy/sim2sim_node.py`: remove entry reset, apply tilt guard.
- `sim2sim/sim2sim_ros2_jazzy/sim2sim_ros2_jazzy/state_machine.py`: bounded damping state.
- `sim2sim/sim2sim_ros2_jazzy/sim2sim_ros2_jazzy/cli.py`: runtime outcome fields.
- `sim2sim/README.md`: playback controls and reset/protection behavior.
- `test/test_sim2sim_walk_state_machine.py`, `test/check_sim2sim_walk_state_machine.py`: entry continuity, command propagation and injected-fall checks.
- This date directory's `support_velocity_sim2sim_*` evidence. The incremental diff and final file hashes are recorded separately. Training-source hashes match the active training launch provenance; no trainer, learner, reward, checkpoint weight or hardware installation was modified.

## Direct evidence

- Export: 256 PyTorch/ONNX samples, max action error 2.86102295e-6, in `support_velocity_sim2sim_prepare.log`.
- Actual ROS/MuJoCo/ONNX manual/headless cases: PASS, 30 and 20 checks respectively. Manual qpos, qvel and simulation time at first policy inference exactly matched the state before the RL request. The reset spy observed no policy-entry resets. All support commands and nonzero vx/yaw reached actor inputs. Injecting 56-degree roll produced damping, no additional policy evaluation, cleared commands/actions and no reset. See `support_velocity_sim2sim_runtime.json`.
- State-machine unit tests: 3 passed. Command-cap regression: 5 passed. Walk regression: 8 passed and 1 conditional skip requiring the Isaac Torch interpreter. Logs use the corresponding `*_tests.log` names.
- The complete CLI was run for 500 control ticks in mode 2 with zero command and with [0.25,0,0.25]. Both completed finite physics and closed cleanly. Zero command remained in RL with no tilt faults, but final x was about 1.37 m, so this is not evidence of good stationary position hold. The moving-command case exceeded 55 degrees and ended in damping with one fault: interface/protection execution PASS, sustained locomotion from the prepared posture FAIL for this trial. See `support_velocity_sim2sim_zero_cli.log` and `support_velocity_sim2sim_cli.log`.
- `support_velocity_sim2sim_agent_check.log`: final repository syntax/XML/whitespace/directory checks.

An initial attempt to prepare directly toward the nominal training joint pose produced about -38-degree pitch at RL entry and subsequent falls. A separate zero-feedforward preparation trial also failed. Those diagnostic results are preserved; neither change is retained. Final preparation uses the original stable SIT controller and only removes the hidden RL-entry reset. Learned rise/transition/tracking quality remains a separate limitation; no stability claim is inferred from protocol checks.

## Reproduction

```bash
python3 sim2sim/sim2sim_ros2_jazzy/launch/sim2sim.launch.py \
  --ckpt mj_lab/logs/flash_sac/tita_mjlab_194029_719452/model_15000 \
  --support-mode 2
```

Use the keys in the terminal that launched playback. No GUI or robot controller was launched automatically for the user. Hardware behavior is NOT_TESTED. The existing training process remains running.
