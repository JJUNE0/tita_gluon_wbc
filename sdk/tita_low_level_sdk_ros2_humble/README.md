# TITA Direct-Mode Sim-to-Real Stack for ROS 2 Humble

Experimental, fail-closed ROS 2 control stack for replacing the vendor TITA locomotion runtime
with one Direct-Mode `ros2_control` hardware/controller owner.

This repository is a research snapshot, **not a safety-certified robot controller**. A process
crash, SBC failure, CAN failure, or ROS shutdown callback is not an emergency stop. Operate only
with physical support, immediate access to the approved full-power cut procedure, and an operator
who understands the Direct-Mode recovery limitations.

## What is included

```text
direct_ws/src/tita_stage1_controller
  single C++ ros2_control command owner
  official TransformUp -> standing settle -> RL -> SAFE_HOLD

lowlevel_ws/src/tita_low_level_sdk
  inert launch, preflight, operator-arm gate, takeover supervisor, async logger

upstream_overlay/ddt_ros2_control
  only files changed from DDTRobot/ddt_ros2_control at the pinned commit

ros2.repos
  exact upstream source pin
```

The repository does not contain the custom ONNX policy, robot logs, SSH credentials, sudoers
configuration, build products, or raw CAN reimplementations.

## Runtime architecture

```text
TITA full power ON
-> vendor MCU stack establishes exact FSM idle
-> command-free preflight
-> explicit operator approval
-> stop tita-bringup.service
-> prove vendor ROS/CAN writers are gone
-> run the exact official upstream start.bash once
-> Direct Mode
-> one HardwareBridge and one controller_manager
-> one Stage1Controller command owner
-> measured-pose official TransformUp
-> five continuous standing seconds
-> bounded policy entry
-> RL_RUNNING
-> deterministic SAFE_HOLD
-> operator-supported full TITA power cycle
```

The production invariant is:

```text
vendor motor writer XOR direct motor writer
```

The vendor stack is used before takeover only to establish MCU `idle`. It is not a Direct-mode
sensor, joystick, balance-controller, or command-manager dependency.

## Verified state of this snapshot

- Upstream base: `DDTRobot/ddt_ros2_control` commit
  `e7b32d9746df900680641ff2845ffb0b5ffe99ed`
- Official `start.bash` SHA256:
  `0a2bca4a146f9127ad558b50ca745826cc93ee920f3bb9538521555ea94f97b3`
- Custom policy SHA256 expected by the controller:
  `d53a5b0b69e5382dc5f40909ecaa7481221397aa3b3400c922b13a33576273e6`
- Real Stage 1: official TransformUp, five-second settle, SAFE_HOLD — PASS
- Real Stage 2: zero-command RL for one second — PASS
- Real Stage 3: command gain `0.3`, 29.162 seconds of RL, then the retained angular-velocity
  watchdog entered SAFE_HOLD — SUSPICIOUS, not unrestricted-operation approval
- Last Stage 3: all motor API writes succeeded; persistent approximately 6 Hz pitch/L1/R1
  closed-loop oscillation remains under investigation

See [TEST_STATUS.md](docs/TEST_STATUS.md) and [SAFETY.md](docs/SAFETY.md).

## Policy contract

```text
inputs:
  nn_input0 [1, 33]
  nn_input1 [1, 10, 33]
output:
  nn_output [1, 8]
policy rate:
  50 Hz
```

```text
native/action order: [L1, L2, L3, L4, R1, R2, R3, R4]
observation joint order: [L1, R1, L2, R2, L3, R3, L4, R4]
observation reindex: [0, 4, 1, 5, 2, 6, 3, 7]
action-output mapping: identity
legs: default_joint_angle + action * 0.25
wheels: action * 5.0 velocity target
```

Do not change order, signs, scaling, gains, limits, rate, or actuator semantics without a new
recorded validation.

## Prerequisites

- Ubuntu 22.04 / ROS 2 Humble on the TITA SBC
- `git`, `python3-vcstool`, `python3-colcon-common-extensions`, `rsync`
- ROS 2 control packages used by the package manifests
- network access during the first build for pinned ONNX Runtime 1.19.2 archives
- custom policy installed separately at `/home/robot/tita_policy/policy.onnx`
- vendor TITA runtime available for the initial MCU/idle check

The upstream `tita_robot` package provides architecture-specific libraries. Their licensing and
redistribution terms remain upstream's responsibility; this repository fetches them from the
pinned upstream rather than copying them.

## Prepare the source

Clone this repository anywhere on the development machine, then fetch and overlay the pinned
upstream source:

```bash
./scripts/bootstrap_upstream.bash
```

The resulting layout is intentionally the same as the deployed robot layout:

```text
direct_ws/src/ddt_ros2_control
direct_ws/src/tita_stage1_controller
lowlevel_ws/src/tita_low_level_sdk
```

## Build on ROS 2 Humble

```bash
source /opt/ros/humble/setup.bash
./scripts/build_humble.bash
```

The script builds only the Direct runtime package set and then runs package-select tests. It does
not stop the vendor service, run `start.bash`, open the real HardwareBridge, or command motors.

## Command-free preflight

With the TITA fully power-cycled, vendor service active, exact FSM `idle`, and the robot still in
MCU mode:

```bash
source /opt/ros/humble/setup.bash
source direct_ws/install/setup.bash
source lowlevel_ws/install/setup.bash
./scripts/command_free_preflight.bash
```

Expected result includes:

```text
ready: true
blockers: []
command_output: DISABLED
```

The default launch is inert and unarmed:

```bash
ros2 launch tita_low_level_sdk direct_rl_mode.launch.py
```

Launch arguments alone cannot authorize takeover. Real execution additionally requires a fresh
powered-session ID, all live gates, explicit operator-arm service transition, and the documented
recovery setup. See [SAFETY.md](docs/SAFETY.md); do not infer authorization from this README.

## Controller lifecycle

```text
WAIT_FOR_HARDWARE
-> MEASURE_INITIAL_POSE
-> TRANSFORM_UP
-> STANDING_SETTLE
-> RL_PREPARE
-> RL_BLEND
-> RL_RUNNING
-> SAFE_HOLD / FAULT
```

Stage 1 excludes RL output. Stage 2 requires centered zero command and has a bounded test window.
Stage 3 uses the same controller and writer with the direct Joy path. In this snapshot, processed
`vx/yaw` are clamped to the training envelope and then multiplied by `0.3`; `vy` remains disabled.

## Logging

The 500 Hz hardware path uses a bounded non-blocking queue and a dedicated writer thread. The log
correlates controller target, measured state, final torque, motor API result, observation, policy
action, Joy command, timing, and watchdog state. Do not commit generated run files.

## Recovery limitation

Graceful in-session Direct-to-MCU rollback is not confirmed. SAFE_HOLD does not restore the vendor
stack. The confirmed recovery is physical support followed by a full TITA power OFF/ON and a new
MCU/idle verification. Never automate the power cycle or automatically restart the vendor stack
from Direct mode.

## Documentation

- [Architecture](docs/ARCHITECTURE.md)
- [Safety and operator gates](docs/SAFETY.md)
- [Deployment](docs/DEPLOYMENT.md)
- [Upstream changes](docs/UPSTREAM_CHANGES.md)
- [Verification status](docs/TEST_STATUS.md)
- [Third-party notices](THIRD_PARTY_NOTICES.md)

## License

Original custom code declares Apache-2.0; see [LICENSE](LICENSE). Vendored overlay files are
derivative changes to upstream packages and retain their upstream package declarations and
copyright notices. `tita_description` currently has an unresolved upstream `TODO` license field,
so users must review upstream terms before redistribution.

