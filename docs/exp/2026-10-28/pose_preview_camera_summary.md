# RViz pose preview camera repair and restart

Execution Domain: DESKTOP_DRY_RUN

Evidence Status: PASS for actual wheel zoom and left-drag orbit input.

Policy Checkpoint SHA256: N/A — kinematic URDF visualization; no policy or robot controller.

Branch: `agent/codex/tita-walk`.

The preview configuration omitted the RViz tool list. Added `rviz_default_plugins/MoveCamera` as its first tool and `rviz_default_plugins/Interact` as an alternative, then gracefully closed and relaunched only the isolated preview session. The existing training run was not touched. The source URDF and launcher were not modified.

Changed file: `sim2sim/robot/tita/rviz/pose_preview.rviz`; report/log evidence under `docs/exp/2026-10-28/`. Incremental diff inspected in `pose_preview_camera_changes.diff`. Pre-existing work preserved; no unrelated edits, commit or publication.

Observed metrics / behavior / log summary: the three preview nodes restarted on ROS domain 88, namespace `/tita_pose_preview`; RViz and the joint slider window were placed side by side on the second monitor. Actual X11 wheel-up and left-drag input was delivered to the RViz 3D render pane. Pixel changes within that pane were 39.4% for zoom and 51.5% for orbit; screenshots visually confirm camera movement. Evidence: `pose_preview_camera_verification.json`, `pose_preview_camera_before.png`, `pose_preview_camera_zoom.png`, `pose_preview_camera_orbit.png`. Console: `pose_preview_camera_console.log`.

The preview was restarted at its configured initial pose. Joint values are saved in `pose_before_camera_restart.json`. This remains a static pose preview: physical balance and the pending one-leg training task are NOT_TESTED.

Repository checks are recorded in `pose_preview_camera_agent_check.log`.
