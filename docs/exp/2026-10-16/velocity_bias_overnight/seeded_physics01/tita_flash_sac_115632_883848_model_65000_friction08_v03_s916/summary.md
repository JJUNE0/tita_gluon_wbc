# tita_flash_sac_115632_883848_model_65000_friction08_v03_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a28e8551929d9a4412f571a2e91577da75879477c15d61f0774ab6f05354dff3

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_65000_friction08_v03_s916",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_65000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "friction": 0.8
    },
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
  "initial_physics_sha256": "8804af23bfa87b44fdcb1c8fd300d918d0161f9acc466ddbdcab093edff15789",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.00107225003502844,
  "max_drift_m": 0.010886240253224549,
  "radial_IAE_m_s": 0.04413138163024651,
  "signed_longitudinal_delta_m": -0.0010536682670648106,
  "tail_speed_mean_m_s": -2.872762925706352e-05,
  "tail_speed_rms_m_s": 2.8754723488020415e-05,
  "tail_sensor_speed_mean_m_s": -2.831513264998894e-05,
  "tail_fk_speed_mean_m_s": -2.94706708174233e-05,
  "peak_tilt_rad": 0.05669365452181818,
  "peak_wheel_torque_nm": 0.33194029331207275,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.051767075179520276,
  "final_integral_m_s": 0.051767075179520276,
  "elapsed_wall_s": 10.615803796972614
}
```
