# RMA Teacher 20260808 MuJoCo viewer

- Execution Domain: VALIDATION_SIM
- Evidence Status: PASS (EGL viewer, inference, 5-second zero-command rollout); SUSPICIOUS (entry pose); FAIL (native GLFW viewer initialization)
- Policy checkpoint: run 2026-08-08_16-12-19, model_9999.pt
- Checkpoint SHA256 (prior export record): df81ed501e6b3ebecb67a5819a79be43cd17122ba78bd021db8c392fcb882891
- Actor ONNX SHA256 (verified): caa4645a6b3ff5e608b5705c520f5947eb954b4d8ec38acdc51cec50350e1f27
- Encoder ONNX SHA256 (verified): ed88c5995a7648767621a9cc16001053a696156272eeead07cc2831f833b8352
- Branch: agent/codex/dev_tita_gluon

## Behavior and evidence

Selected the established August 8 teacher baseline. This does not establish it as best across all metrics; the August 19 v5 report has lower zero-command translation drift.

Native MuJoCo passive viewer initialization stalled. A faulthandler trace located the wait in viewer launch and _Simulate initialization. Software GL and no-vsync retries also failed to finish GLFW initialization. All stalled task-owned viewer processes were terminated.

Added test/teacher_mujoco_simple_viewer.py to render the existing simulation node using MuJoCo EGL and a Tk image window. The policy, observation, action, and physics implementations were unchanged. The window follows the robot at 25 FPS maximum; it has no native passive-viewer mouse/keyboard controls. Closing it stops the simulation.

The final viewer logged VIEWER_READY and FSM transitions idle -> reference_transform_up -> reference_stand_hold -> rl_0. After 3 seconds settling, 248 samples over 4.987 seconds showed 0.04168 m planar drift, maximum roll/pitch 1.855 degrees, minimum base height 0.33753 m, and no fall. Entry leg error remained 1.207 rad (SUSPICIOUS). This is a short nominal rollout, not a robustness claim.

Simulation uses local-only ROS domain 91. No hardware actions were performed. Viewer left running at zero velocity command.

Artifacts: teacher_808_egl_viewer.log, teacher_808_egl_eval.log, teacher_808_viewer_metrics.json. Earlier attempts are retained in teacher_808_viewer*.log and teacher_808_simple*.log.

## Checks

- Existing test/eval_rma_zero_command_drift_ros.py: PASS on final EGL viewer; earlier samplers failed to receive topics while native viewer initialization was stalled.
- scripts/agent-check.sh: PASS (see teacher_808_agent_check.log).
- Final task diff inspected; changes consist of the new test viewer and this task's experiment artifacts. Pre-existing worktree modifications were preserved.
