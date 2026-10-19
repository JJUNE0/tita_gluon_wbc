# FlashSAC checkpoint commands for MuJoCo sim-to-sim

Execution Domain: VALIDATION_SIM; regression and launch-interface inspection: DESKTOP_DRY_RUN.

Evidence Status: PASS for ONNX export/parity, MuJoCo script execution, CLI inspection and regression tests. Locomotion quality: SUSPICIOUS; the short zero-command integration probe is not a full policy evaluation. Interactive ROS viewer rollout: NOT_TESTED.

Policy Checkpoint SHA256 (model_15000/actor.pt): `f330e86adeb4b5be2ed276fae01063df63e15bc625d8ad0125746263c42e73a2`.

ONNX SHA256: `6bff36595e34efefd44879eedab9afb95179da89846df576e56bcc6874ab1d76`.

Branch: `agent/codex/dev_tita_gluon`.

The user requested commands to run individual FlashSAC checkpoints in the existing `sim2sim` MuJoCo flow after evaluation. The existing runner consumes ONNX rather than FlashSAC model directories. A dedicated export command now makes each checkpoint usable by that existing runner. No shared MuJoCo runtime, robot configuration, hardware/deployment path or active training settings were changed.

## Data flow and resulting behavior

`model_N/actor.pt` + validated `ddt.json` → deterministic FlashSAC actor → `tanh(mean)` → saved sign-dependent gains → ONNX native-order eight actions → existing MuJoCo `ActionAdapter` native scales/offsets/PD → torque clipping and MuJoCo physics → native actions in `ObservationBuilder.last_action`.

The ONNX input is `nn_input0 [1,33]`; output is `nn_output [1,8]`. It has no history or estimator input. Legacy checkpoints embed unit gains. New checkpoints embed their saved gains, so MuJoCo must retain the original native scales (legs 0.25 rad; wheels 5 rad/s) and must not multiply gains again. The wrapper expresses RMS normalization with ONNX-supported arithmetic, and compares against the original actor's RMS implementation as part of parity validation.

Each export writes `policy.onnx`, `tita_flash_sac.yaml` and `export.json` inside `model_N/exported_flash_sac/`. The generated YAML uses the existing My45c template, current native P_V action semantics and the corrected TITA scene. It starts in the training default joint pose at the existing 0.4-m base reset height, and removes the template's extra gyro low-pass filter to match the direct training observation. PD parameters, torque limits and native scales are retained. Interactive command caps remain 0.2 m/s and 0.3 rad/s. Other original templates and generated model files were not modified.

## Commands

From the repository root, export one checkpoint with the Isaac/PyTorch interpreter. The example checkpoint was actually exported and checked:

```bash
cd /home/cocel/Desktop/Research/tita_gluon_wbc
sac_checkpoint="$PWD/lab/ddt_lab/logs/flash_sac/tita_flash_sac_172127_928297/model_15000"
/home/cocel/isaac/env_isaaclab/bin/python lab/ddt_lab/scripts/flash_sac/export.py \
  --checkpoint "$sac_checkpoint"
```

To export all complete checkpoints from this run:

```bash
sac_run="$PWD/lab/ddt_lab/logs/flash_sac/tita_flash_sac_172127_928297"
for sac_checkpoint in "$sac_run"/model_*; do
  [ -f "$sac_checkpoint/ddt.json" ] || continue
  /home/cocel/isaac/env_isaaclab/bin/python lab/ddt_lab/scripts/flash_sac/export.py \
    --checkpoint "$sac_checkpoint" || break
done
```

Select the step to view, then activate the existing MuJoCo/ROS environment:

```bash
cd /home/cocel/Desktop/Research/tita_gluon_wbc
sac_step=15000
sac_checkpoint="$PWD/lab/ddt_lab/logs/flash_sac/tita_flash_sac_172127_928297/model_$sac_step"
source /home/cocel/venvs/cosim_ros2_jazzy/bin/activate
source /opt/ros/jazzy/setup.bash
source "$PWD/sim2sim/install/setup.bash"
export ROS_LOG_DIR="$PWD/docs/exp/2026-10-14/flash_sac_mujoco_ros_logs"
ros2 launch cosim_ros2_jazzy tita_mujoco_sim2sim.launch.py \
  config:="$sac_checkpoint/exported_flash_sac/tita_flash_sac.yaml" viewer:=true
```

In a second terminal, source the same virtual environment, ROS setup and workspace setup, then begin from the same policy-default pose:

```bash
ros2 topic pub --once /tita/command/manager/cmd_key std_msgs/msg/String '{data: pose_stand}'
ros2 run cosim_ros2_jazzy keyboard_command_node
```

After the pose reset, `0` enables RL. Use `w/s` for forward/backward, `a/d` for yaw and `r` to return commands to zero. `1` runs the reference stand-up trajectory and reaches a different entry posture; use the explicit `pose_stand` route above for checkpoint comparisons. Close the viewer before changing the selected checkpoint.

For repeatable headless checks, invoke the existing Python-only probe, retaining output under `docs/exp`:

```bash
PYTHONPATH="$PWD/sim2sim/cosim_ros2_jazzy" \
  /home/cocel/venvs/cosim_ros2_jazzy/bin/python \
  sim2sim/cosim_ros2_jazzy/scripts/probe_zero_command_drift_mujoco.py \
  --config "$sac_checkpoint/exported_flash_sac/tita_flash_sac.yaml" \
  --settle_s 1 --hold_s 20 \
  > "docs/exp/2026-10-14/tita_flash_sac_expanded_${sac_step}_zero_cmd.log" 2>&1
```

Add `--walk_vx 0.2 --walk_ramp_s 0.4 --walk_cruise_s 3 --walk_decel_s 0.4` to test walk-stop with the training command ramp rate 0.5 units/s. Give that output a separate `_walk_stop.log` filename. This existing probe records displacement and joint positions; it does not establish a statistically measured fall rate or exact command tracking across trials.

## Executed validation

- New export command on model_15000: **PASS**, ONNX checker and native PyTorch/ONNX Runtime parity on 256 observations. Maximum absolute output difference **5.0962e-6**. The validation subprocess uses the already-installed MuJoCo environment's ONNX Runtime; Isaac Sim startup and new dependency installation are unnecessary.
- Existing `inspect_onnx.py`: **PASS**, input `nn_input0 [1,33]`, output `nn_output [1,8]`.
- Existing `probe_zero_command_drift_mujoco.py`, settle 0.2 s, hold 2 s: **PASS for execution**, observed drift **0.1057 m**, base height minimum **0.4005 m**, final **0.4322 m**. This confirms the export-to-MuJoCo path executes; it does not claim good standstill performance.
- `ros2 launch ... --show-args`: **PASS** with logs redirected inside the workspace using ROS_LOG_DIR. An initial read-only filesystem failure at the default external ROS log path was resolved by redirecting logs. No ROS simulator node, keyboard command, topic publisher or hardware command was started by this check.
- `python -m unittest discover -s test -p 'test_flash_sac*.py' -v`: **41 tests PASS**, including three new export tests for signed gains, native-scale/last-action agreement, compiled weight prefixes and legacy unit-gain behavior.
- Required repository check and task-relative source-integrity result are recorded in `tita_flash_sac_mujoco_agent_check.log`.

Direct logs: `tita_flash_sac_mujoco_export_console.log`, `tita_flash_sac_mujoco_export_tests.log`, `tita_flash_sac_mujoco_export_probe.log`, `tita_flash_sac_mujoco_launch_args.log`. The export command also generated its timestamped JSON and summary under `docs/exp/2026-10-14/`.

Changed sources: new `lab/ddt_lab/scripts/flash_sac/export.py`; updated FlashSAC `README.md`; new `test/test_flash_sac_export.py`. Existing dirty source changes were retained, and no shared sim2sim source was edited. The active FlashSAC training process continues independently.

The existing MuJoCo PD controller does not model the training actuator-delay or reset IMU/encoder-bias randomization. This flow evaluates transfer to the current clean MuJoCo model. Export/parity success and the two-second probe are separate from full sim-to-sim locomotion validation. Hardware deployment was not part of the task.
