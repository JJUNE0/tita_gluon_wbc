# Third-party notices

## DDTRobot/ddt_ros2_control

This repository fetches source from:

```text
https://github.com/DDTRobot/ddt_ros2_control.git
commit e7b32d9746df900680641ff2845ffb0b5ffe99ed
```

Files under `upstream_overlay/ddt_ros2_control` are modifications to files from that project and
retain the copyright notices and package license declarations of their upstream counterparts.

Relevant upstream package declarations at the pinned commit include:

- `hardware_bridge`: Apache-2.0
- `teleop_command`: Apache License 2.0
- `ros_utils`: Apache License 2.0
- `tita_robot`: MIT
- `tita_description`: upstream package metadata says `TODO: License declaration`

The architecture-specific `tita_robot` shared libraries and TITA meshes are fetched from upstream;
they are not duplicated in this repository. Users are responsible for verifying that their use
and redistribution comply with upstream and vendor terms.

## ONNX Runtime

The controller build downloads the official ONNX Runtime 1.19.2 prebuilt archive selected by CPU
architecture and validates the pinned SHA256 in CMake. ONNX Runtime is distributed under the MIT
license by Microsoft Corporation.

## ROS 2

ROS 2 and ros2_control components retain their respective upstream licenses. They are external
dependencies and are not vendored here.

