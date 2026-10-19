# TITA Static Elevation Capture

- Date: 2026-07-29
- Execution Domain: `ROBOT_READ_ONLY`
- Policy Checkpoint SHA256 / ONNX Hash: `N/A` (sensor-only rosbag capture)
- Evidence Status: `PASS`
- Bag ID: `tita_static_20260729_073023`
- Remote path: `/home/robot/bags/tita_elevation/tita_static_20260729_073023`
- Local path: `/home/cocel/tita_elevation_bags/tita_static_20260729_073023`

## Observed Metrics

- Storage: SQLite3/CDR
- Size: 916.6 MiB (`du`: 917M)
- Duration: 12.941741368 s
- Total messages: 13,452
- `/tf`: 702
- `/tf_static`: 1
- `robot_description`: 1
- left/right image: 347 / 205
- left/right CameraInfo: 129 / 130
- face/neck SPAD: 163 / 161
- IMU: 5,481
- chassis odometry: 650
- joint states: 5,482

All requested topics have a nonzero message count. Remote ROS 2 Humble and local ROS 2 Jazzy `ros2 bag info` outputs agree on size, duration, total count, and per-topic counts.

The unequal left/right image counts are suspicious and agree with the earlier live stereo rate/skew finding. Static TF, robot description, and both CameraInfo streams are present, so offline frame and calibration reconstruction data was captured.

## Safety and Scope

The recorder only subscribed to sensor/state/TF topics. No command topic was published, no service/action was called, and no robot process or configuration was changed. Playback has not been attempted yet (`NOT_TESTED`).
