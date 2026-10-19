# tita_flash_sac_115632_883848_model_65000_kick-0.2_v03_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a28e8551929d9a4412f571a2e91577da75879477c15d61f0774ab6f05354dff3

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_65000_kick-0.2_v03_s917",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_65000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 917,
    "estimator": "fk",
    "guarded": true,
    "kick": -0.2,
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
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
  },
  "checkpoint_sha256": "a28e8551929d9a4412f571a2e91577da75879477c15d61f0774ab6f05354dff3",
  "onnx_sha256": "7cc289e8aee44513f1e29487c7522e96c762174e2444aedaa7aea78b3a66a3ec",
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
  "initial_physics_sha256": "8a7543f4a5c8ceb60651fb07f7f9a753a67a22b34956a7d1184b0175550cf2c3",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.004573230120908656,
  "max_drift_m": 0.08088118997596729,
  "radial_IAE_m_s": 0.3735434341472601,
  "signed_longitudinal_delta_m": -0.004519361474755631,
  "tail_speed_mean_m_s": -2.4825975298992318e-05,
  "tail_speed_rms_m_s": 2.4853057530814982e-05,
  "tail_sensor_speed_mean_m_s": -2.4550616757648852e-05,
  "tail_fk_speed_mean_m_s": -2.5735384001556722e-05,
  "peak_tilt_rad": 0.08216576534246167,
  "peak_wheel_torque_nm": 1.5092334747314453,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.04975124069031245,
  "final_integral_m_s": 0.04975124069031245,
  "elapsed_wall_s": 11.840624034986831
}
```
