# TITA portfolio interface capture

- Date: 2026-09-09
- Execution Domains: `TRAINING_SIM`, `VALIDATION_SIM`, `ROBOT_READ_ONLY`, `DESKTOP_DRY_RUN`
- Policy Checkpoint SHA256: `3766e05c683d6f2565bbeb2c21f500f872b243ffe39fb48b40fd3ae7ff608ef8`
- ONNX Hash: `ecb0fd3ec56eb9aed5349250e9de11040156f59e3a98c54ae83dadde672a7705`
- Evidence Status: `SUSPICIOUS` overall; individual captures are `PASS` for UI visibility, while live REAL2SIM state is intentionally `BLOCKED`

## Observed metrics / behavior / log summary

- Isaac Sim 5.1 opened the TITA play scene and displayed the parallel environment stage under `World/envs`.
- CoSim v1.5.0 displayed environment, policy/ONNX, randomization, command, and keyboard-input controls.
- MuJoCo loaded the TITA corrected scene for the SIM2SIM and REAL2SIM viewer captures.
- The read-only REAL2SIM node started with `/tita4252763` as the configured state namespace and published `mapping_ok: false` in isolated local DDS because no joint/IMU/odometry source was present.
- No physical robot connection, TCP relay, ROS command publisher, service call, or motor command was started.
- The direct ROS2 policy-node path remains `SUSPICIOUS` due to the pre-existing `ObservationBuilder.include_base_height` interface mismatch in the dirty worktree.

## 32-env Isaac Lab follow-up

- Execution Domain: `TRAINING_SIM` / `DESKTOP_DRY_RUN`
- Command: `scripts/rsl_rl/play.py --task=DDT-Velocity-Flat-Tita-My-Play-v0 --checkpoint=model_2700.pt --num_envs=32 --device=cuda:0`
- Runtime evidence: Isaac Sim reported `app ready`, `Number of environments: 32`, `Environment spacing: 2.5`, and completed checkpoint loading plus ONNX/TorchScript export.
- Screenshot artifact: `docs/portfolio/captures/tita_isaaclab_32_envs.png` (`1920×1080`, SHA256 `be828845d74984fa0a25ee87ef1552a8a547bef82a9b9d49c0e1b43a47cec17d`)
- Evidence Status: `PASS` for the 32-env scene/UI capture; `SUSPICIOUS` for performance claims because Isaac Sim emitted CPU powersave/IOMMU, PhysX/Fabric, and GPU memory-budget warnings.

## Artifacts

- Portfolio index: `docs/portfolio/README.md`
- Overview: `docs/portfolio/captures/tita_interface_overview.png`
- Capture set: `docs/portfolio/captures/`
