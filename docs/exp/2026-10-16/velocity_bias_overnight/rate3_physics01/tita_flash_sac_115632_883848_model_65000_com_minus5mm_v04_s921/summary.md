# tita_flash_sac_115632_883848_model_65000_com_minus5mm_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a28e8551929d9a4412f571a2e91577da75879477c15d61f0774ab6f05354dff3

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_65000_com_minus5mm_v04_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_65000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "com": -0.005
    },
    "law": {
      "kp": 0.0,
      "ki": 4.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 3.0,
      "seed_gain": 3.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
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
  "initial_physics_sha256": "bf1d7810b6d6ad0e71f1e351534aa928367fe8be8576ccda0342eeebf15f4b51",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.007096353146669896,
  "max_drift_m": 0.011896101745465732,
  "radial_IAE_m_s": 0.4692039571293811,
  "signed_longitudinal_delta_m": 0.007066843666792919,
  "tail_speed_mean_m_s": -2.552217167227681e-05,
  "tail_speed_rms_m_s": 2.5617373775064873e-05,
  "tail_sensor_speed_mean_m_s": -2.5249869998688632e-05,
  "tail_fk_speed_mean_m_s": -2.619690505461935e-05,
  "peak_tilt_rad": 0.056963675328193464,
  "peak_wheel_torque_nm": 0.24574410915374756,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.014072656690261398,
  "final_integral_m_s": 0.014072656690261398,
  "elapsed_wall_s": 6.238563191029243
}
```
