# Student 0809 native MuJoCo viewer

- Execution Domain: VALIDATION_SIM
- Evidence Status: PASS (native viewer and model initialization); NOT_TESTED (native-viewer keyboard rollout)
- Policy checkpoint: 2026-08-09_15-40-20/model_999.pt
- Policy Checkpoint SHA256: e37f6c1936d699627afb109ef141138958a3f0890028c1c8e1c107056b4a8b10 (previously verified)
- Actor ONNX SHA256 (verified): caa4645a6b3ff5e608b5705c520f5947eb954b4d8ec38acdc51cec50350e1f27
- Adaptation ONNX SHA256 (verified): 490c21e247bdf15858873211b5d8d833918cda4fb819cb9fb9fcf6a49976718d
- Branch: agent/codex/dev_tita_gluon

User selected native MuJoCo viewer with separate terminal keyboard control. Stopped the task-owned custom viewer and removed its newly created script. No existing source files changed. Launched tita_mujoco_sim2sim.launch.py with tita_moo_stand_drive_20260809_999_rma_student.yaml, viewer=true, keyboard=false, joystick=false, local-only ROS domain 96. Native MuJoCo window and complete policy initialization confirmed by logs and X window tree. Left in initial idle state for operator keyboard start (1, wait for reference_stand_hold, then 0).

Earlier custom-viewer test of the same policy completed 249 samples over 4.987 seconds: planar drift 0.00816 m, minimum height 0.33740 m, no fall; entry error 1.207 rad remains SUSPICIOUS. Custom keyboard injection did not establish reliable key handling and was superseded by user-requested standard terminal keyboard node. These results do not validate native keyboard rollout or robustness.

Artifacts: student_0809_native_viewer.log; earlier student_0809_keyboard* logs and metrics retained as trial evidence. No robot commands performed.

Checks: ./scripts/agent-check.sh PASS; final task artifacts reviewed, changes limited to experiment records. Native terminal keyboard control is provided for operator execution, not automatically run.
