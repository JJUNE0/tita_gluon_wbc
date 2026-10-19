# August 19 Teacher v5 MuJoCo viewer

- Execution Domain: VALIDATION_SIM
- Evidence Status: PASS (viewer and short rollout); SUSPICIOUS (entry pose)
- Run: 2026-08-19_18-43-03_rma_teacher_deployable_obs_v5_10k/model_9999.pt
- Checkpoint SHA256 (export record): 020ae1d400ea14c85ecf33210ee76ec2d44ffc03cd0132de0b4cd719cc3dc1b6
- Actor ONNX SHA256 (verified): 4913cd9612aeafcc8f51cfe31dc45014ab9725ef29d5c343cb5fbbe23cbf984e
- Encoder ONNX SHA256 (verified): 6de7a0daae71fdf57177a4f4d29f53b8c91a367b01aeaa5d81c16ad0a15b4a83
- Branch: agent/codex/dev_tita_gluon

Stopped the previous August 8 viewer and launched the existing EGL/Tk viewer with tita_moo_stand_drive_20260819_9999_rma_teacher_deployable_obs_v5.yaml. Local-only ROS domain 92; no hardware commands. Window title updated using X properties to identify August 19 v5. No source files changed.

VIEWER_READY and rl_0 confirmed in teacher_819_egl_viewer.log. Existing test/eval_rma_zero_command_drift_ros.py completed successfully after a 3-second settle: 250 samples over 5.006 seconds, planar drift 0.01689 m, minimum height 0.35029 m, maximum roll/pitch 1.954 degrees, no fall. Entry error warning remains 1.207 rad. This short nominal run does not establish robustness. Viewer left running with zero velocity command.

Artifacts: teacher_819_egl_viewer.log, teacher_819_egl_eval.log, teacher_819_viewer_metrics.json, teacher_819_agent_check.log.

Validation: evaluator PASS; agent-check.sh PASS. Final task artifacts reviewed; only this task's experiment records added, pre-existing files preserved.
