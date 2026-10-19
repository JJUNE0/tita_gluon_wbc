# RMA teacher deployable-observation v5 model 9999 sim2sim

- Date: 2026-08-20
- Execution Domain: `VALIDATION_SIM`
- Evidence Status: `SUSPICIOUS`
- Run: `2026-08-19_18-43-03_rma_teacher_deployable_obs_v5_10k`
- Checkpoint: `model_9999.pt`
- Checkpoint SHA256: `020ae1d400ea14c85ecf33210ee76ec2d44ffc03cd0132de0b4cd719cc3dc1b6`
- Actor ONNX SHA256: `4913cd9612aeafcc8f51cfe31dc45014ab9725ef29d5c343cb5fbbe23cbf984e`
- Teacher encoder ONNX SHA256: `6de7a0daae71fdf57177a4f4d29f53b8c91a367b01aeaa5d81c16ad0a15b4a83`
- Robot model: TITA-only corrected MuJoCo model (`nq=15`, `nu=8`)

## Interface verification

The saved training configuration sets `num_policy_stacks=0` and removes
`base_lin_vel_x`, `base_lin_vel_y`, `base_lin_vel_z`, and `base_height` from
`stack_policy`. The deployed actor contract is therefore:

```text
actor observation 32 (proprio 28 + normalized command 4)
teacher latent 16
actor input 48 -> action 8
```

The teacher-only encoder contract is:

```text
privileged observation 26 -> latent 16
```

The privileged vector is contact 2, mass 1, CoM 3, actuator Kp 8, actuator
Kd 8, body-frame base linear velocity 3, and base height 1. Ground-truth base
velocity and height are absent from the actor observation and remain only in
the teacher encoder path, as intended for subsequent student distillation.

The actor and encoder were exported directly from `model_9999.pt`. ONNX
reference evaluation agreed with the checkpoint-backed PyTorch modules with
maximum absolute errors of `9.54e-7` and `5.96e-8`, respectively. The run
directory's pre-existing `exported/policy.onnx` differed from the final
checkpoint actor by up to `0.2944` on a fixed random input and was therefore
not used.

## Validation

- Config/runner interface validation: `PASS`
- Privileged-observation 25D backward-compatibility and 26D extension tests:
  `PASS` (`2 passed`)
- ROS package symlink build: `PASS`
- Policy and encoder load in MuJoCo: `PASS`
- FSM path `idle -> reference_transform_up -> reference_stand_hold -> rl_0`:
  `PASS`
- Zero-command policy execution for 10 seconds: `PASS` (no fall)

Zero-command metrics after a 3-second RL settle period:

| Metric | Result |
|---|---:|
| Planar drift, 5 s | 0.01676 m |
| Planar drift, 10 s | 0.03617 m |
| Mean horizontal speed | 0.00364 m/s |
| Yaw drift, 10 s | 1.42 deg |
| Maximum absolute roll/pitch | 1.95 deg |
| Minimum base height | 0.35029 m |
| Fall detected | no |

Raw metrics are in
`rma_teacher_deployable_obs_v5_model9999_zero_drift.json`.

## Suspicious observations and limits

The existing ad-hoc reference stand pose produced an RL-entry leg position
error warning with maximum absolute error `1.207 rad`. The policy recovered
and stayed upright, but this transition mismatch must be resolved or bounded
before using the result as a Sim2Real readiness claim. This is one
deterministic nominal-dynamics rollout and does not establish robustness to
mass, friction, sensor noise, latency, or actuator mismatch.
