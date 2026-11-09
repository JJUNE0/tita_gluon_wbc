# TITA single Sim2Real workspace

Execution Domains: `DESKTOP_DRY_RUN` for local builds/tests;
`ROBOT_STATE_CHANGING` for operator-invoked launch. Canonical workspace:
`sim2real/tita_ws` locally, `~/tita_ws` after a separately approved robot deployment.
No per-checkpoint workspaces are needed.

## Current policy pair

| Policy | Bundle | Source checkpoint SHA256 |
|---|---|---|
| Frozen Teacher80k | `flashsac_mjlab_pose_80000` | `5487e3584fddbdfc87b7485bb2ad4c7da8069a7679b1975789d64419e7482334` |
| Experiment2 torque residual10k + LPF60 | `20261109/10000_d6672529ee24/residual` | `d6672529ee247a92b7043f50bb6deb501a65becbf760761a412b33d5701b6002` |

Policy selection is [`../config/policies.json`](../config/policies.json),
relative to that JSON. Actual files are in `../checkpoints/`, organized as
`<framework>/task/<family>/<task>/<YYYYMMDD>/<step>/`. The residual entry contains
both `policy.pt` (matching Teacher) and `residual.policy.pt`, plus saved contracts.
The native source package no longer has duplicate `policies/` bundles.

The controller source is the latest hardware-tested full-pose/direct-joystick
version. Public launch validates the pinned Teacher config/ONNX and residual
manifest/ONNX before creating the logged hardware runner. A new policy requires
an explicit export and contract validation; changing a filename alone is insufficient.

## Public entrypoints

After deployment, from the robot workspace, the start script sources ROS and
this workspace automatically. It checks workspace `config/policies.json`, then
adjacent source config, then the installed config. `TITA_POLICY_CONFIG=/path/to/policies.json`
selects a different config:

```bash
cd ~/tita_ws
./start_sim2real.sh false teacher   # output disabled; still accesses hardware
./start_sim2real.sh true teacher
./start_sim2real.sh true residual
```

Equivalent commands after sourcing ROS and `install/setup.bash`:

```bash
ros2 launch tita_controller sim2real.launch.py output_enabled:=true
ros2 launch tita_controller sim2real.residual.torque.launch.py output_enabled:=true
```

`policy_config:=/path/to/policies.json` overrides selection in ROS launch.
Checkpoint paths resolve relative to that JSON. The installed package preserves
this same config/checkpoints layout. Rebuild/redeploy to refresh its installed
copy; editing an adjacent source config is picked up on the next start-script run.

Only these two public launch files remain. `_policy_launch.py`,
`_controller_nodes.py` and `_residual_bundle.py` implement shared validation and
node construction; operators should use the public launchers. `run_sim2real.sh`
retains the existing logged runner, Ready→Direct MCU precondition, owned process
groups, recorder and shutdown sequence. Do not invoke the private node helper
as a replacement for that sequence.

## Control behavior

- With motor output enabled, only the500Hz motor/control thread requests
  `SCHED_FIFO` priority20 and timer slack1ns. Startup prints the verified active
  settings; a setup failure prevents normal control and uses the existing
  bounded shutdown-zero path. Output-disabled runs keep their original scheduling.
  SDK frame waits remain100us and TX remains synchronous. Policy, CAN receive
  and capture-publisher threads keep their existing scheduling. For an explicit
  comparison, prefix the same start command with `TITA_MOTOR_RT_PRIORITY=0`;
  default/unset or `20` selects RT. Other values are rejected. The corresponding
  `motor_realtime_priority` ROS parameter is read-only after startup. Full
  policy/ROS-load timing with this setting still needs hardware validation.
- `vx=-axes[2]*1.5m/s`, `yaw_rate=axes[3]*3rad/s`, subject to deadzone and saved
  limits. Stick changes apply immediately; there is no velocity slew ramp.
- Right stick `-axes[0]` roll and `-axes[1]` pitch; `axes[5]` height speed/hold.
  Pose ranges: roll ±30°, pitch ±15°, height 0.27–0.42m, nominal 0.335m.
  Saved pose ramp rates are retained.
- The existing prepare/sit/RL/software-stop button state machine is unchanged.
  Follow the startup button instructions printed by the controller.
- In residual mode, `axes[7]=0` permits residual; ±1 disables it. Teacher remains
  active in RL either way. Residual additionally requires exact-zero requested
  and applied velocity, valid sensors, and pose within the trained ranges.
  Roll/pitch commands and nonnominal heights are permitted within those bounds.
- Teacher50Hz / residual250Hz run in the policy worker; the nonwaiting motor
  exchange targets500Hz. Residual is held between worker results. PD + residual
  is effort-clipped once; the residual expires after12ms and Teacher after40ms
  from its source snapshot. Existing generation/fault checks remain unchanged.
- Experiment2 uses its saved60Hz residual-only one-pole LPF on every500Hz motor
  tick, including held250Hz actor requests. Fresh PD is added after filtering,
  then the final effort limit is applied. Filter state clears immediately when
  residual is disabled, stale, from a different gate epoch, or outside valid RL.
  No synthetic training torque delay is added on hardware.
- Residual uses the same measured gyro/gravity/leg-joint sample as the Teacher
  builder, mapped to its saved native440-input frame. Wheel displacement uses
  shared measured leg angles/gravity and the actual wheel encoder. No synthetic
  training noise/bias is injected on hardware. Actor previous-output history
  remains the selected requested torque before the LPF.
- Actuator samples separately record `selected_residual` (requested),
  `filtered_residual` (candidate feedforward after LPF) and `computed_torque`
  (after PD sum/clamp), with `residual_lpf_hz`. `torque_sent` records transport
  acceptance separately. These are not motor actuation acknowledgements.

Residual actor250Hz, Teacher50Hz and motor/filter500Hz remain the trained timing
contract.500Hz actor inference is not a launch-time override: changing it also
changes the observation history's time span and the policy's closed-loop behavior.

## Build and evidence

Local ROS Jazzy build (no physical controller launch):

```bash
cd sim2real/tita_ws
source /opt/ros/jazzy/setup.bash
source install/setup.bash
colcon build --packages-select tita_controller --allow-overriding tita_controller \
  --cmake-args -DBUILD_TESTING=OFF -DPython3_EXECUTABLE=/usr/bin/python3
```

For a standalone robot `~/tita_ws`, the separately approved deployment should
copy this workspace plus `sim2real/config/` and `sim2real/checkpoints/` into
`~/tita_ws/config/` and `~/tita_ws/checkpoints/`. CMake supports both this standalone
layout and the repository's adjacent layout; the config's relative paths stay valid.

For a fresh workspace with no install tree, build dependencies using
`--packages-up-to tita_controller` instead. On the robot use its installed
ROS distribution (currently Humble). Local compilation does not deploy anything. CMake installs the shared
`sim2real/checkpoints/` tree and its config with the controller. Automatic play
registration creates local copies in both domains without selecting/deploying them.
Only a validated hardware export can be selected for a physical launch; see the
[registry instructions](../checkpoints/README.md).

The runner records under workspace `docs/exp/YYYY-MM-DD/`: summary, console,
ROS logs and rosbag. Actuator capture defaults ON at the500Hz motor-loop sampling
clock (`/sim2real/actuator_sample`). Worker samples and Teacher/residual/command
streams remain recorded. These are timestamped controller samples and cached SDK
feedback, not proof of fresh500Hz sensor packets or a motor torque ACK.
Shutdown attempts ten zero-torque commands with the original fault guards.

Older staged workspaces, launchers and policy bundles were moved into
`docs/exp/2026-11-08/backup/` at the repository root (see the backup manifest).
Historical paths/scripts require restoration before reuse. Existing robot
workspaces have not been removed or overwritten by this local cleanup.
