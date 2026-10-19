# FlashSAC SBC commands and mandatory logs

Current entrypoint (updated on both PC and SBC): source ROS/workspace, then
`ros2 launch tita_controller flashsac.launch.py`. It now stops bringup automatically
and starts mandatory logs/rosbag before the controller. The manual-stop sections
below describe the earlier workflow. See the current
[single-command launch report](flashsac_launch_auto_stop.md) and workspace README.

- Execution Domain: ROBOT_READ_ONLY (inspection), DESKTOP_DRY_RUN (runner preparation/tests).
- Evidence Status: PASS for SSH inspection and subsequent SBC deployment/build; robot runtime NOT_TESTED.
- Date: 2026-10-16 (Asia/Seoul)
- Branch: agent/codex/dev_tita_gluon
- Policy Checkpoint SHA256: `6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05`
- ONNX Hash: `f44f07ed44970e3ff565eae67fd9229adf0be5c02215591c52a691ffcbb71b2a`

## Inspected state

SSH: `robot@192.168.0.28`, host `tita`, home `/home/robot`, ROS `/opt/ros/humble`.
The existing workspace is `/home/robot/tita_ws`; `/home/robot/flashsac_60000_ws`
was absent. Existing `ros2_control_node` PID 941 and joystick PID 1075 both belong
to `tita-bringup.service`, which is active and enabled. `tita-perception.service`
is also active. CAN `can0` is UP, CAN FD 1 Mbit/s arbitration / 5 Mbit/s data;
UART `/dev/ttyTHS1` is present. These are interface configuration observations,
not evidence of actuator torque correctness.

`colcon`, `ament_cmake`, `ament_cmake_auto`, `generate_parameter_library`,
`realtime_tools`, `rosbag2_transport` and SQLite storage packages are available.
No service was stopped, no files copied to the SBC, and no CAN/UART socket,
robot controller or actuator command was started by this task.

Inspection logs: [environment](flashsac_sbc_inspection.log),
[services/dependencies](flashsac_sbc_services.log).

Current workspace: `/home/robot/tita_ws`, replaced and built under the user's
subsequent authorization. See [SBC build report](flashsac_sbc_build.md).
The initial transfer/build instructions below are historical and must be skipped
for this already-installed workspace. Use `~/tita_ws` for subsequent sessions;
the earlier proposed `~/flashsac_60000_ws` location was not deployed.

Current source archive SHA256: `6e3ed6d41e910f8289a4347e881b66d049511821286a27c6ac4b85c074ee27ce`.

## 1. PC: transfer the prepared source archive

The following commands are operator instructions; transfer/build have not been executed.

```bash
# DESKTOP_DRY_RUN / ROBOT_STATE_CHANGING (remote file deployment)
cd /home/cocel/Desktop/Research/tita_gluon_wbc
scp sim2real/tita_ws/build/flashsac_60000_sbc_source.tar.gz robot@192.168.0.28:~/
ssh robot@192.168.0.28
```

## 2. SBC: create isolated workspace and build

Run in the SSH terminal. Use a fresh workspace; do not overwrite the existing
`~/tita_ws`. If `mkdir` reports an existing directory, inspect it before extracting.

```bash
# ROBOT_STATE_CHANGING: source deployment/build; no controller launch
mkdir ~/flashsac_60000_ws && tar -xzf ~/flashsac_60000_sbc_source.tar.gz -C ~/flashsac_60000_ws
cd ~/flashsac_60000_ws
source /opt/ros/humble/setup.bash
exp_dir="$PWD/docs/exp/$(TZ=Asia/Seoul date +%F)"
mkdir -p "$exp_dir"
set -o pipefail
colcon --log-base "$exp_dir/colcon" build --packages-up-to tita_controller --cmake-args -DBUILD_TESTING=OFF -DPython3_EXECUTABLE=/usr/bin/python3 2>&1 | tee "$exp_dir/flashsac_build_$(date +%H%M%S).log"
```

Continue only if the build returns zero and finishes all four packages. Then:

```bash
source install/setup.bash
export ROS_LOG_DIR="$exp_dir/ros"
ros2 launch tita_controller flashsac.launch.py --show-args 2>&1 | tee "$exp_dir/launch_arguments.log"
```

## 3. SBC: operator-controlled session

Support the robot before stopping its existing controller. The commands below
change runtime state and are for the operator to execute. Stopping the existing
service is necessary even for output-disabled testing because the new launch also
opens the joystick UART. The script does not stop services itself.

```bash
# ROBOT_STATE_CHANGING: stop existing control and joystick together
sudo systemctl stop tita-bringup.service 2>&1 | tee -a "$exp_dir/operator_commands.log"
# ROBOT_COMMAND_FREE_RUNTIME: controller torque output remains off
./run_flashsac.sh false
```

After Ctrl+C ends the output-disabled session, use this command for an explicitly
operator-approved motor-output session:

```bash
# ROBOT_STATE_CHANGING
./run_flashsac.sh true
```

Joystick: left up = idle (original velocity damping); left down + right up =
transform-up; wait for `state: sit`, then right middle/down = RL. Startup switch
position is ignored. Left up returns to damping; it does not hold the ready pose.
An early RL request is rejected; reselect it after `sit`. Ctrl+C ends the launch
and closes the recording. Service restart is also an operator action; when ready
to return to the original stack, `sudo systemctl start tita-bringup.service`.

For a new SSH terminal before running, always use:

```bash
cd ~/flashsac_60000_ws
source /opt/ros/humble/setup.bash
source install/setup.bash
./run_flashsac.sh false
```

## Logs and validation

Every runner invocation records its summary/exit code, console, ROS logs and
policy hashes inside `~/flashsac_60000_ws/docs/exp/YYYY-MM-DD/` using Korea time.
Successful recorder startup produces a SQLite rosbag containing:

- `/tita4252763/joint_states`, `/tita4252763/imu_sensor_broadcaster/imu`, `/tita4252763/joy`
- `/sim2real/debug/{obs,action,torque,state}`, `/rosout`

The torque topic is computed command torque, not measured hardware torque.
No recording means no launch; a recorder that exits causes controller shutdown.
`NOT_TESTED` in the generated summary is intentional: process exit status alone
does not prove correct robot behavior. Add observed behavior and assessment after
the run. Copy logs back from another PC terminal:

```bash
# DESKTOP_DRY_RUN: collect remote logs into the repository
cd /home/cocel/Desktop/Research/tita_gluon_wbc
scp -r robot@192.168.0.28:~/flashsac_60000_ws/docs/exp/. docs/exp/
```

Changed files: `sim2real/tita_ws/run_flashsac.sh`, workspace README,
`test/sim2real/test_flashsac_logging.py`, this report, the setup report's archive
hash, inspection/test logs, and refreshed delivery archive. Existing controller
and policy source files were not changed in this logging task.

- `bash -n sim2real/tita_ws/run_flashsac.sh`: PASS.
- `python3 test/sim2real/test_flashsac_logging.py`: PASS, 5 tests using a mock CLI
  without ROS processes, CAN/UART access or actuation. Tests cover console/summary
  creation and recorder finalization, output selection, existing-controller refusal,
  storage startup failure and recorder exit while the controller is running.
  [Log](flashsac_logging_tests.log).
- `python3 -m py_compile test/sim2real/test_flashsac_logging.py`: PASS.
- Required `./scripts/agent-check.sh`: FAIL, exit 1, from the same pre-existing
  trailing whitespace in `lab/ddt_lab/ddt_lab/tasks/manager_based/locomotion/robots/tita/my_flat_env_cfg.py`
  at lines 431, 437, 443, 449, 455 and 461. Syntax checks: PASS, 462 files;
  URDF checks: PASS, 8 files. [Log](flashsac_logging_agent_check.log).
- Final script/doc diff integrity checks: PASS. Archive contents match current
  runner, README and ONNX bytes. Tracked diff SHA256 is unchanged:
  `40076fca037839dbd955f4644f404a0e3ea6c8b5e7a3fc86a79bb15150ddab47`;
  no files staged, committed or pushed.

The subsequent Humble ARM build passed; see the linked SBC build report.
Actual rosbag recording, actuator signs/units and runtime timing: NOT_TESTED.
Existing unrelated source changes are preserved.
