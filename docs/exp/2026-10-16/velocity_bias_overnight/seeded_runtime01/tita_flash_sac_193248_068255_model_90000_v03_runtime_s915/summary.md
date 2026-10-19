# tita_flash_sac_193248_068255_model_90000_v03_runtime_s915

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d94ec425dcab69bfb8001711468b6ca37297f4e1aec2e9b20535fd106ee98769

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_90000_v03_runtime_s915",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_90000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 915,
    "estimator": "fk",
    "runtime": true,
    "law": {
      "kp": 0.0,
      "ki": 4.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0,
      "seed_gain": 3.0
    },
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0",
    "controller_source_sha256": "6056e5bd50e0d84e7e554e390f2ede0726c82adf059af80911969c1286a3cded"
  },
  "checkpoint_sha256": "d94ec425dcab69bfb8001711468b6ca37297f4e1aec2e9b20535fd106ee98769",
  "onnx_sha256": "aff309a07b913000eb7916a9b3867232296f7834f48d5391c16e7ec4e09b84d2",
  "input_columns": [
    "velocity_bias_m_s",
    "filtered_velocity_m_s",
    "integral_m_s"
  ],
  "state_columns": [
    "base_x",
    "base_y",
    "base_z",
    "base_forward_speed",
    "roll",
    "pitch",
    "yaw",
    "raw_position",
    "raw_speed",
    "fk_position",
    "fk_speed"
  ],
  "initial_physics_sha256": "2b86fe9af3881f3d80a78b5ee1a10eeeaf383db071ff29d5693cbfe0553f9c87",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.09143846773272023,
  "max_drift_m": 0.10903470479281986,
  "radial_IAE_m_s": 5.160540699312731,
  "signed_longitudinal_delta_m": 0.09143791247118314,
  "tail_speed_mean_m_s": 0.00015960500185006356,
  "tail_speed_rms_m_s": 0.00016074903143227032,
  "tail_sensor_speed_mean_m_s": 0.00015953137170358726,
  "tail_fk_speed_mean_m_s": 0.00016093229147109018,
  "peak_tilt_rad": 0.10221105566001287,
  "peak_wheel_torque_nm": 1.6700465679168701,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.6406959345722586,
  "final_integral_m_s": 0.6406959345722586,
  "elapsed_wall_s": 16.272702207032125
}
```
