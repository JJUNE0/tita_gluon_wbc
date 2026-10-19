# tita_ws (sim2real)

TITA real-robot runtime with the same structure as `sim2sim/sim2sim_ros2_jazzy`:
one node, one loop, one state machine, and the same exported policy folder.

| sim2sim (`sim2sim_ros2_jazzy/`) | sim2real (`src/tita_controller/`) |
|---|---|
| `state_machine.py` | `include/tita_controller/state_machine.hpp` |
| `adapter.py` | `include/tita_controller/adapter.hpp` |
| `sim2sim_node.py` + `mujoco_env.py` | `src/tita_node.cpp` + `tita_robot` CAN API |
| keyboard `1` / `0` / `6` | joystick switches (below) |

Vendor packages copied unchanged from `tita_gluon_ws/src/ddt_ros2_control`:
`tita_robot` (CAN API, prebuilt), `teleop_command` (ELRS joystick -> `sensor_msgs/Joy`), `ros_utils`.

## Frozen FlashSAC model_50000

Execution domains: `DESKTOP_DRY_RUN` for local build/tests;
`ROBOT_STATE_CHANGING` for the public launch, which stops the existing service
even with controller torque output disabled (the default).

The selected checkpoint is
`lab/ddt_lab/logs/flash_sac/tita_flash_sac_115632_883848/model_50000`.
Its exported actor is included in `src/tita_controller/policies/flashsac_50000/`
and installed with the package. The original checkpoint/export is left unchanged.
The previous `policies/flashsac_60000/` bundle is retained. Restoring the old
launch and runner together is required to select it and keep pinned hashes and
run identifiers consistent; a deployment backup contains the previous install.
`flashsac.launch.py` verifies pinned ONNX/config/checkpoint hashes before creating nodes;
it needs no PC training-log path on the SBC. The policy consumes 33 observations,
produces eight native-order actions, and runs at 50 Hz inside the 500 Hz motor loop.
The frozen ONNX actor includes its trained action gains. No residual, RLS, probing,
or runtime gain/bias/reference adaptation is present.

Read-only SSH inspection confirmed Ubuntu 22.04, `/opt/ros/humble`, and existing
workspace `/home/robot/tita_ws`. The user approved replacing `/home/robot/tita_ws` with this workspace.
The previous workspace is archived outside the active path before replacement. Both the existing motor controller and joystick are owned by
`tita-bringup.service`. The replacement/build operation does not stop or launch controllers.
Build in the replacement workspace:

```bash
cd ~/tita_ws
source /opt/ros/humble/setup.bash
exp_dir="$PWD/docs/exp/$(TZ=Asia/Seoul date +%F)"
mkdir -p "$exp_dir"
set -o pipefail
colcon --log-base "$exp_dir/colcon" build --packages-up-to tita_controller --cmake-args -DBUILD_TESTING=OFF -DPython3_EXECUTABLE=/usr/bin/python3 2>&1 | tee "$exp_dir/flashsac_build_$(date +%H%M%S).log"
source install/setup.bash
```

Source the rebuilt workspace, support the robot, then use one launch command.
It validates the frozen policy, stops `tita-bringup.service`, waits for its
controller/joystick to disappear, starts logging and rosbag, then launches the
new controller. With `output_enabled:=true`, it first sends the upstream
`start.bash` MCU Ready -> Direct request sequence after recording is ready;
failure prevents controller startup. `output_enabled:=false` sends no MCU mode
requests. Successful request transmission is logged separately from a mode ACK,
which the current SDK does not expose. Service stop uses exactly `sudo -n /usr/bin/systemctl stop
tita-bringup.service`; failure prevents the new controller from starting.
Existing SBC permission for this command was inspected; permissions were not changed.

```bash
# ROBOT_STATE_CHANGING: automatic service stop, new controller torque output off.
source install/setup.bash
ros2 launch tita_controller flashsac.launch.py
```

After ending that session with Ctrl+C, the operator can select physical actuation:

```bash
# ROBOT_STATE_CHANGING
ros2 launch tita_controller flashsac.launch.py output_enabled:=true
```

The runner always saves console output, ROS logs, checkpoint/ONNX/config hashes,
exit status and a rosbag under this workspace's `docs/exp/YYYY-MM-DD/` (Korea date).
It starts the recorder first, rejects launch if recording cannot start, stops
the launch if recording exits, and finalizes the bag on Ctrl+C. The recording
contains joint states, IMU, joystick, observation, action, computed torque, state
and rosout. Use `namespace:=<name>` to override the namespace. The environment
hook loaded by `install/setup.bash` also places the outer ROS launch logs under
`docs/exp/YYYY-MM-DD/ros/`. The existing `./run_flashsac.sh false|true` commands
delegate to this public launch. The installed logged runner calls generic
`tita.launch.py` internally, avoiding launch recursion. The old service is never
restarted automatically, including on launch failure or Ctrl+C.
The inner launch and recorder each run in an owned process session with SIGINT
restored to its default disposition. Ctrl+C signals each owned process group,
then escalates to SIGTERM/SIGKILL with bounded waits if descendants remain.
Wait for the runner's `Exit ...; saved: ...` message before starting another run.
Duplicate-process refusal prints the conflicting PID and command. Existing
processes from older runs are never killed automatically during a new launch.

The default namespace is `tita4252763`.
The main controller and policy inference run on the SBC. Build ARM binaries there;
do not copy the desktop's `build/` or `install/` directories. Do not run another
motor controller alongside this node. SBC build, CAN ownership, physical torque
signs/units and joint mapping must be checked on the SBC; desktop parity is not
hardware validation.

For observation/action/torque inspection, the controller publishes
`/sim2real/debug/{obs,action,torque,state}`. Torque is the computed command in
native order (left leg_1..4, right leg_1..4), before `output_enabled` gating;
it is not measured/applied torque. The expected joint-space unit is N*m.

Desktop checks (no robot node or CAN API is instantiated):

```bash
source /opt/ros/jazzy/setup.bash
python3 test/sim2real/test_sim2real_parity.py sim2real/tita_ws/src/tita_controller/policies/flashsac_50000
python3 test/sim2real/test_flashsac_setup.py --torch-python /home/cocel/anaconda3/envs/online_rl/bin/python
```

## Build

```bash
cd sim2real/tita_ws
source /opt/ros/<distro>/setup.bash
colcon build      # downloads ONNX Runtime 1.19.2 for x86_64 or aarch64
```

If another Python (e.g. Isaac) is first in `PATH`, build with the system Python
(`catkin_pkg` must be importable).

## Run

Copy the sim2sim export folder of a checkpoint (`<model>/sim2sim/actor/`: `config.json` + `policy.onnx`)
to the robot. Run `sim2sim.launch.py --prepare-only` first if it does not exist yet.

```bash
source install/setup.bash
# read-only: reads CAN/IMU/joystick, publishes state, sends no torque
ros2 launch tita_controller tita.launch.py policy_dir:=<actor folder>
# motors on
ros2 launch tita_controller tita.launch.py policy_dir:=<actor folder> output_enabled:=true
```

## States and joystick

### Optional zero-command velocity bias

```bash
# Computes policy + bounded correction and records it; motor output remains off.
ros2 launch tita_controller flashsac.launch.py velocity_bias:=true
```

`velocity_bias` defaults to false. When enabled, an encoder/IMU/relative-FK
observer and a torque-bounded integral law run at policy cadence inside the
existing controller. Each neutral hold ignores 0–1 s, estimates drift and mean
pitch over 1–3 s with correction OFF, and applies correction after 3 s. It changes only the
two native wheel velocity targets before their existing PD and torque clipping.
The same eight-element torque vector is sent once per 500 Hz loop; this mode
does not create another CAN sender. Actor observations and raw last actions
are unchanged.

The additional computed torque is fixed at **+/-0.8 Nm per wheel**, converted
using the actual wheel Kd and radius (the larger Kd sets the shared bias bound).
Integral gain 4 and LPF tau 0.1 s are retained; the `3*v` torque seed is removed.
A 1 s ramp and slew of at most **0.8 Nm/s per wheel** bound application.
The integral tracks the limited output to prevent hidden windup. With the
selected checkpoint the common velocity-offset bound is +/-0.148 m/s; final
policy-plus-bias wheel torque is still clipped at +/-12 Nm.
`velocity_bias_max_torque` and its old environment variable remain unsupported;
the 0.8 Nm limit is fixed. Movement commands, RL exit and invalid timing cut
the correction immediately and reset acquisition. During acquisition/application,
tilt above 0.3 rad or estimated speed above 1 m/s inhibits correction. After
acquisition, pitch deviation above **5 degrees** from the 1–3 s mean also cuts
correction and latches it OFF until movement-command exit/reentry or RL reset.
The node logs the acquired drift/pitch reference and inhibition transitions.
Hold hysteresis is the same as sim2sim:
enter below [0.02, 0.02, 0.03], leave at [0.04, 0.04, 0.06].

`velocity_bias_response_sign:=1.0` uses the MuJoCo closed-loop response sign;
hardware feedback sign, sensor alignment, slip and actual torque calibration
remain NOT_TESTED. `-1.0` is the alternate response sign. The sign is
validated before the public launch creates the runner. This is an adaptive
velocity offset with an integral state; it does not use RLS, LQR gains or
probing and does not hold absolute position or heading.

The runner always records the selection, bias limit/slew, sign and geometry hash.
`/sim2real/debug/velocity_bias` contains 11 values:
`holding, eligible, hold_age_s, v_hat_m_s, filtered_v_m_s, integral_m_s,
bias_m_s, wheel_offset_L_rad_s, wheel_offset_R_rad_s,
actual_added_computed_torque_L_Nm, actual_added_computed_torque_R_Nm`.
The existing torque topic records the final computed eight-joint torque.
Output-disabled mode computes the same signals without transmitting torque.

`/sim2real/training_sample` (`tita_controller/msg/TrainingSample`) records a single
frame at the same nominal 50 Hz policy cadence, plus state transitions. It also
records invalid-sensor frames, with an empty observation and validity flags.
Each frame has a ROS stamp captured just after the controller sensor read,
`sequence_id` (starts at zero on node restart), `control_tick` (2 ms loop index),
and `monotonic_ns` for measuring intervals even if wall/ROS time changes. Existing
JointState/IMU stamps use that same frame stamp. These are controller snapshot
times, not hardware CAN acquisition times. Sequence gaps indicate missing
training frames; account for node restarts and bag subscription startup.

The frame includes observation, command, joint/IMU state, raw ONNX action,
wheel velocity offsets, equivalent `teacher_action`, computed torque, bias
diagnostics, state, and validity/output/transport flags. `teacher_action` is in
**ONNX output units including export gains**, not normalized actor units:
`physical_target = clip(action_raw * scale + offset) + wheel_velocity_bias`,
then `teacher_action = (physical_target - offset) / scale`. Only wheels receive
the velocity offset. Divide by checkpoint export gains when fitting the
normalized actor. `teacher_action_valid` checks current inference and adapter
invertibility/target clipping; actor output bounds must additionally be checked
offline. It does not certify good behavior or hardware actuation.

For physical teacher-data training, select RL frames with `sensors_valid`,
`policy_valid`, `teacher_action_valid`, `output_enabled` and `torque_sent` true,
then apply command/bias/quality filters for the task. `torque_sent` means the
transport call accepted the command, not a motor acknowledgement or measured
torque. The observation's last-action fields retain the existing raw-action
convention. Collection and subsequent student execution must account for this
history convention. The logged runner records the new topic automatically.
Build this package on the SBC and source its overlay before collection; desktop
builds are not deployed to the robot automatically.

`idle` (start, original velocity damping) -> `transform_up` (current -> splay -> sit)
-> `sit` -> `rl`. Left release from RL starts `return_to_sit`, which interpolates
directly from the measured pose to sit over 2 s, then settles for 0.2 s.
The return also blends from the previous computed torque to the sit PD torque.
Idle retains the original damp behavior: `torque[i] = clip(-Kd[i] * joint_velocity[i])`,
with `Kd = [8, 8, 8, 0.5, 8, 8, 8, 0.5]` and checkpoint torque limits.
Stationary joints receive zero torque; moving joints receive opposing damping torque.
An internal `sit` state holds the ready pose after transform-up until the operator
selects RL. Same transform poses, gains and timings as sim2sim. `rl` is rejected
until `sit`; policy inference starts only in `rl`.

The left lower button is a latching RL selector. The right lower button is held
for startup and pressed again for an immediate software stop; its release alone
does not stop. There is no long-press action on the left button.

| State | Button action | Result |
|---|---|---|
| Startup | Both buttons released | Arm recognition of a fresh startup hold |
| Idle (or initial fault damping after sensors recover) | Left up, hold right for at least 1 s | `transform_up` then `sit` |
| Transform/sit/RL/return | Release the startup right-button hold | Continue current state |
| Sit | Push left down | `rl` |
| RL | Push left again so it comes up | `return_to_sit` then `sit` |
| After startup was enabled | A new right-button press | Latched `estop`, original velocity damping |

Starting with either button held cannot start movement; release both first.
A short right press in idle cancels without starting. Keeping the startup press
held cannot also trigger stop; release it and press again to stop. A new right
press has priority over a simultaneous left action. Joystick loss/invalid data
after enabling also latches stop. `estop` cannot be cleared by joystick or fault
requests; restart the process with both buttons released to begin again.
It is a software damping stop, not electrical power isolation or zero torque.

Default node parameters `left_button_axis=4`, `right_button_axis=6` follow the
DDT two-position channel convention (down=-1, up=+1). This physical mapping is
NOT_TESTED and must be confirmed with output disabled before hardware deployment.
Middle/unknown button values are invalid. The old axes[4]/axes[5] three-position
switch scheme is no longer used by this controller.

RL still requires `sit`; an early left press does not queue automatic RL entry.
Release/repress left after `state: sit`, including when a sit-return was still
running. Sit completion is time based and does not prove the robot attained its
target or that it can balance without the policy. Sticks remain `axes[2]` for
forward/back and `axes[3]` for yaw, with checkpoint caps and 0.5/s ramp in RL.
Command and previous action are cleared outside RL.

Safety: stale or non-finite IMU/motor data, or tilt > 0.65 rad, switches to `damp`
(legs and wheels: velocity damping only). Torques are clipped to the checkpoint torque limits.
Fault handling takes precedence over joystick requests in the same tick.
Invalid policy tensor shapes/timing reject startup; non-finite observations/actions
or inference errors enter `damp`. A fault during an enabled session requires
process restart/re-preparation before further RL; no automatic RL resume occurs.

Button/state regression (no ROS/CAN API): `python3 test/sim2real/test_joystick_buttons.py`.

Published for `real2sim`: `/<namespace>/joint_states`, `/<namespace>/imu_sensor_broadcaster/imu`,
and `/sim2real/debug/{obs,action}` at the policy rate.
