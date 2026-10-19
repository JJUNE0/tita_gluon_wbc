# tita_flash_sac_115632_883848_model_65000_tau0.2_entry12

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a28e8551929d9a4412f571a2e91577da75879477c15d61f0774ab6f05354dff3

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_65000_tau0.2_entry12",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_65000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 271,
    "estimator": "fk",
    "runtime": true,
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.2,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
    }
  },
  "checkpoint_sha256": "a28e8551929d9a4412f571a2e91577da75879477c15d61f0774ab6f05354dff3",
  "onnx_sha256": "7cc289e8aee44513f1e29487c7522e96c762174e2444aedaa7aea78b3a66a3ec",
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
  "initial_physics_sha256": "12ca94e455b99e23372ac0081f1f704358ba2a78ac3b5e267c82a2acd1ca4ddb",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.004796701690297805,
  "max_drift_m": 0.011444278724895155,
  "radial_IAE_m_s": 0.30833754745407393,
  "signed_longitudinal_delta_m": 0.004787195551900362,
  "tail_speed_mean_m_s": -9.284304846180064e-06,
  "tail_speed_rms_m_s": 9.297218284626659e-06,
  "tail_sensor_speed_mean_m_s": -9.047851272481573e-06,
  "tail_fk_speed_mean_m_s": -1.0232496304554667e-05,
  "peak_tilt_rad": 0.05723672626936116,
  "peak_wheel_torque_nm": 0.31944113969802856,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.04966340041705795,
  "final_integral_m_s": 0.04968234622495811,
  "elapsed_wall_s": 5.933188294991851
}
```
