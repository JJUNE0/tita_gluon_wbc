# RMA Student model_999 sim-to-sim validation

- Execution Domain: `VALIDATION_SIM`
- Evidence Status: `SUSPICIOUS`
- Source run: `/home/cocel/Desktop/Research/isaaclab_add_reward_autotuning/logs/co_rl/Tita_Flat_Stand_Drive-v3-mooppo/mooppo/2026-08-09_15-40-20`
- Policy class: `RMAStudent`
- Checkpoint: `model_999.pt`
- Checkpoint SHA256: `e37f6c1936d699627afb109ef141138958a3f0890028c1c8e1c107056b4a8b10`
- Actor ONNX SHA256: `caa4645a6b3ff5e608b5705c520f5947eb954b4d8ec38acdc51cec50350e1f27`
- Adaptation encoder ONNX SHA256: `490c21e247bdf15858873211b5d8d833918cda4fb819cb9fb9fcf6a49976718d`
- Config: `sim2sim/cosim_ros2_jazzy/config/tita_moo_stand_drive_20260809_999_rma_student.yaml`

## Interface evidence

- `params/agent.yaml`: `class_name=RMAStudent`, `history_len=50`, `latent_dim=16`, `num_policy_stacks=1`, `empirical_normalization=false`.
- Actor ONNX: `obs[1,84] -> actions[1,8]`.
- Adaptation encoder ONNX: `history_in[batch,50,36] -> z_hat[batch,16]`.
- Each 36-dim history frame matches training: current `stack_policy[32]` plus `none_stack_policy[4]` command.
- Config selects `policy.architecture: rma_student`; the teacher config selects `rma_teacher`. No source edit is needed to switch between them.

## Tests and observations

1. Python syntax and direct ONNX contract smoke: `PASS`.
   - Student rolling history shape `(50,36)` verified.
   - Two consecutive student actions and one teacher action were finite and shaped `(8,)`.
2. ROS2 package build: `PASS`.
   - `colcon build --symlink-install --paths cosim_ros2_jazzy --packages-select cosim_ros2_jazzy`
3. Headless startup smoke, 20 s: `PASS`.
   - Correct student architecture and both ONNX hashes logged.
   - No traceback, ONNX interface error, or node crash.
   - Log: `test/eval_logs/rma_student_20260809_999_headless.log`
4. Headless closed-loop policy execution: mechanical execution `PASS`, behavior `SUSPICIOUS`.
   - Entry sequence: `pose_stand -> rl_0` (direct simulation reset/handoff, not the long reference transform-up path).
   - Sample: state `rl_0`, policy tick `687`, sim time `15.86 s`.
   - Finite action sample, maximum absolute component `0.8362`.
   - Base position: `[1.8483, 0.2891, 0.1553] m`.
   - Base RPY: `[-3.0228, 0.0740, 0.9884] rad`.
   - The robot had rolled over by the sample time despite inference continuing without an exception.
   - Log: `test/eval_logs/rma_student_20260809_999_closed_loop_metrics.log`

## Interpretation and unresolved risks

The student export and config-selected inference path are operational, but this run is not behaviorally stable in the tested direct handoff. The result does not isolate whether the fall comes from the student adaptation quality, the MuJoCo/Isaac dynamics gap, or the direct `pose_stand -> rl_0` handoff. The separately documented open-loop `reference_transform_up` instability also remains unresolved. No robot hardware, networking, or robot command path was used.
