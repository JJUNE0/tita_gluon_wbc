# TITA RViz pose preview

Execution Domain: DESKTOP_DRY_RUN

Evidence Status: PASS for GUI startup, rendered model/TF and live joint-state reception. Physical balancing and the proposed one-leg training environment are NOT_TESTED.

Policy Checkpoint SHA256: N/A — static URDF visualization, without a policy or controller.

Branch: `agent/codex/tita-walk`.

## Result

Per the user's follow-up, open RViz first so they can demonstrate the desired pose before finalizing the one-leg task. The RViz and Joint State Publisher windows are running on display `:0`, arranged side by side on the second monitor. The original training process and training source files were left unchanged.

The preview uses the existing TITA URDF and absolute mesh URIs. Six virtual joints, generated in memory, expose body x/y/z and yaw/pitch/roll; the eight robot joints remain available. These virtual joints only move the visualization. The source URDF was not edited. RViz displays a world-fixed ground grid and the robot's visual meshes.

The three preview processes are `robot_state_publisher`, `joint_state_publisher_gui` and `rviz2`. Their ROS domain is 88 with localhost-only discovery, namespace `/tita_pose_preview`; TF and joint-state topics are namespaced. No robot control nodes or command publishers were started.

tmux: `tita_pose_preview_20261028`.

Log: `pose_preview_console.log`; ROS logs: `pose_preview_ros_logs/`.

Run again from the repository root:

```bash
source /opt/ros/jazzy/setup.bash
python3 sim2sim/robot/tita/launch/pose_preview.launch.py
```

Controls:

- `joint_left_leg_1..3` and `joint_right_leg_1..3`: leg joints, radians.
- `joint_*_leg_4`: wheel angles.
- `preview_base_x/y/z`: body translation, meters.
- `preview_base_roll/pitch/yaw`: body rotation, radians.
- `Center`: restore the configured initial pose.

Observed metrics / behavior / log summary: all three nodes started; RViz initialized OpenGL 4.6 and the rendered robot's Global Status is OK. A read-only subscriber received 14 finite joint/body positions, including nominal leg positions approximately `[0, 0.8, -1.5, 0]` on each side and body z approximately 0.4 m. Evidence: `pose_preview_verification.json`, `pose_preview_rviz.png`, `pose_preview_sliders.png`. The screenshots were inspected directly.

This is kinematic pose visualization; it does not simulate gravity, floor collisions or stability. The existing wheel URDF limits span many turns, so wheel sliders cover a much wider range than leg sliders.

## Files and checks

- Added `sim2sim/robot/tita/launch/pose_preview.launch.py`.
- Added `sim2sim/robot/tita/rviz/pose_preview.rviz`.
- Added this report and verification/log artifacts under `docs/exp/2026-10-28/`.

Actual GUI startup and read-only ROS subscription: PASS. Source URDF and inspected training files unchanged. Pre-existing repository edits were preserved. No commit, push, publication or hardware execution was performed.

Agent-check result is recorded separately in `pose_preview_agent_check.log`.

## Pending environment work

The user confirmed that the desired vertical support axis means the hip-center to wheel-center line. The proposed `stand_one_leg_env_cfg.py` is still pending the pose demonstration. Its requested behavior is zero velocity commands, a two-second left/right gait cycle and a 0.5-second swing window per foot, while using the body and opposite leg for balance. No one-leg learning run has been started.
