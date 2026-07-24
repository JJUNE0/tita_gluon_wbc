# Changes relative to DDTRobot/ddt_ros2_control

## Base

```text
repository: https://github.com/DDTRobot/ddt_ros2_control.git
commit: e7b32d9746df900680641ff2845ffb0b5ffe99ed
```

The `upstream_overlay/ddt_ros2_control` tree contains only files changed from that commit. The
bootstrap script refuses a different upstream HEAD before applying the overlay.

## HardwareBridge

- immutable hardware-output gate plus controller-owned command-enable gate
- direct joint/IMU/motor freshness and finite-state interfaces
- motor-status availability separated from all-online status
- final software PD torque clamp
- motor API return checking and consecutive write-failure propagation
- controller-to-writer sequence and final-command correlation
- bounded asynchronous 500 Hz writer logger with flush acknowledgment
- HardwareBridge plugin regression test

## TITA description

- hardware output and wheel torque-limit xacro parameters
- ros2_control state/command GPIO interfaces used for safety and logger correlation
- Direct joint, IMU, motor-feedback, and writer-status exposure

## Direct Joy reader

- receive-only/joy-only mode
- no vendor command-manager or SDK command publication in Direct operation
- explicit UART/configuration parameters used by the Stage 2/3 launch

## Unmodified official Direct request

`start.bash` is not present in the overlay because it must remain byte-identical to the pinned
upstream file. The supervisor checks its exact SHA256 before the one permitted invocation.

