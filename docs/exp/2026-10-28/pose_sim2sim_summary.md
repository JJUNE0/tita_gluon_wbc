# Roll/pitch/height command playback and latest completed checkpoint

- Execution Domains: VALIDATION_SIM and DESKTOP_DRY_RUN.
- Evidence Status: PASS for export, observations, command ramps, keyboard/HUD flow and finite runtime. Long-duration tracking quality is not established; hardware behavior NOT_TESTED.
- Branch: `agent/codex/tita-walk`.
- Requested checkpoint: `mj_lab/logs/flash_sac/tita_mjlab_202755_365015/model_15000`.
- Requested Policy Checkpoint SHA256: `60d0251f0bb27667ef2ce9d3ce3c04624044862bdeec9b9779e739b399b310a5`.
- Latest completed checkpoint verified during this task: `mj_lab/logs/flash_sac/tita_mjlab_202755_365015/model_75000`.
- Latest Policy Checkpoint SHA256: `c5aa083797d198464f3823f083f155b216c3ef5e52d66439b36ff8a05b37ff10`.
- Latest ONNX SHA256: `30b773ac4a218f31637fda09b529870e056dd1c20a32b504cf9abf284aad4de3`.
- Selection time and actor/native-config/playback-config hash checks: `pose_sim2sim_latest_selection.json` and selection console evidence.

## Resulting behavior

The saved `base_pose` generated command is now represented as a distinct `pose_commands` observation. Its three values are roll radians, pitch radians and absolute base_link height metres, with saved scales/order/clipping. This model is 38-input/8-action, but its last three inputs are not the same-width support-mode one-hot command. Old observation layouts retain their meaning.

The checkpoint defines current ranges of roll +/-30 degrees, pitch +/-15 degrees and height 0.27–0.42 m, nominal 0/0/0.335, with rates 0.15 rad/s, 0.15 rad/s and 0.02 m/s. No duplicate pose range or rate is added to YAML. The runtime begins at nominal pose, freezes the emitted pose during preparation, and advances once after each RL physics step. Target requests remain latched. The previous no-respawn policy-entry behavior is retained.

`--pose ROLL_DEG PITCH_DEG HEIGHT_M` works for viewer and headless invocation. CLI degrees are converted to radians before feeding the policy. Out-of-range/nonfinite CLI requests are rejected. The simulation Vector3 topic `/tita/command/manager/cmd_pose` uses radians/radians/metres; its finite targets are clipped to the saved bounds. Invalid ROS samples do not change the target.

Keyboard controls in the launching terminal: `1` prepare, `0` RL; `j/l` roll +/-1 degree, `i/k` pitch +/-1 degree, `u/o` height +/-1 cm, `p` nominal target; existing vx/yaw controls remain. `r` stops velocity without changing pose target. Explicit `2` resets physics and restores nominal pose. The viewer displays target, emitted and actual pose. Residual wheel controllers are rejected for pose-command policies because those adapters do not implement commanded-pose semantics.

## Changed files

- `sim2sim/sim2sim_ros2_jazzy/sim2sim_ros2_jazzy/checkpoint.py`: command-name resolution, saved contract validation and inference metadata.
- `sim2sim/sim2sim_ros2_jazzy/sim2sim_ros2_jazzy/adapter.py`: optional pose input and correct raw actor values.
- `sim2sim/sim2sim_ros2_jazzy/sim2sim_ros2_jazzy/sim2sim_node.py`: bounded targets, saved-rate update, ROS/keyboard controls and HUD.
- `sim2sim/sim2sim_ros2_jazzy/sim2sim_ros2_jazzy/cli.py`: pose argument forwarding and outcome telemetry.
- `sim2sim/README.md`: units, controls and invocation.
- `test/test_mjlab_roll_pitch_height.py`: replace the old expected-rejection assertion with the now-supported interface assertion; other pre-existing test content preserved.
- `test/test_sim2sim_pose.py`, `test/check_sim2sim_pose.py`, `test/check_pose_command_parity.py`: scoped contract/runtime/ramp checks.
- `pose_sim2sim_*` evidence in this date directory. The task's incremental diff and final hashes are in `pose_sim2sim_changes.diff` and `pose_sim2sim_verification.json`.

Training code and checkpoint weights were not modified. Protected training hashes match the initial snapshot. No trainer was stopped/restarted, no hardware code was deployed, no GUI window was launched, and no commits/publication occurred.

## Executed validation

| Check | Direct evidence | Result |
|---|---|---|
| Contract/observation/CLI unit tests | 7 tests; saved order/units, absolute height, invalid inputs, old support one-hot, viewer/headless CLI forwarding | PASS |
| Existing native pose tests | 13 tests, including native observation/reset/reward checks | PASS |
| 15k export | 256 PyTorch/ONNX samples, max action error 3.09944153e-6 | PASS |
| Latest 75k export | 256 PyTorch/ONNX samples, max action error 4.88758087e-6 | PASS |
| Actual 15k and 70k runtime probes | Each ran 648 ONNX calls and 15 checks: entry continuity, nominal first pose, bounds, signed targets, ramped actor inputs, explicit reset, keyboard loop and HUD calls | PASS |
| Native command parity | 641 recorded production runtime samples compared with the actual training RollPitchHeightCommand on CPU; maximum command error 0.0 | PASS |
| Latest complete CLI | 500 finite control ticks with `--pose 10 -5 0.35`; final target/emitted values agree, state remains RL | PASS for execution |
| Command-cap / walk / state-machine regression | 5 + 8 + 3 passed, 1 conditional Isaac-Torch skip | PASS for executed cases |
| Actual support runtime regression | Existing manual/headless support and tilt/no-reset protocol cases | PASS |
| Final agent check | `pose_sim2sim_agent_check.log` | See final direct log |

The initial viewport/HUD probe found a missing `quat_wxyz_to_rpy` import; it was fixed and both actual checkpoint probes were rerun successfully. Initial failure evidence is retained in `pose_sim2sim_15000_runtime_initial.*`. The HUD check uses a fake passive viewer handle and real terminal key-loop logic; it does not open a GUI window.

The 70k CLI trial ended at approximately roll 0.0958 rad, pitch -0.0530 rad and height 0.3803 m for a target of 10 degrees, -5 degrees and 0.35 m. These are observed policy tracking errors, not proof of accurate posture tracking. Extended accuracy, robustness and hardware behavior need separate evaluation. The implementation carries commands and the saved observation/action semantics; it does not change the learned controller.

## User command

```bash
python3 sim2sim/sim2sim_ros2_jazzy/launch/sim2sim.launch.py \
  --ckpt mj_lab/logs/flash_sac/tita_mjlab_202755_365015/model_75000 \
  --pose 0 0 0.335
```

This selects the latest completed checkpoint checked during this task. Angles in this CLI argument are degrees and height is metres. The first two keys remain `1`, then `0` after preparation completes.
