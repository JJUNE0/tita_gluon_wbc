# tita_flash_sac_115632_883848_model_65000_com_minus5mm_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a28e8551929d9a4412f571a2e91577da75879477c15d61f0774ab6f05354dff3

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_65000_com_minus5mm_v02_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_65000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "com": -0.005
    },
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.1,
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
  "initial_physics_sha256": "ac5a7a7ba4ba02dab5c81e786ed334a70e7f97254aac23a9d2d26d114ed06eb8",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.0016342680349786276,
  "max_drift_m": 0.0026362632556234176,
  "radial_IAE_m_s": 0.1108174373500115,
  "signed_longitudinal_delta_m": 0.0014738211236921762,
  "tail_speed_mean_m_s": -9.782724544796793e-06,
  "tail_speed_rms_m_s": 9.824194919595438e-06,
  "tail_sensor_speed_mean_m_s": -9.543196002805791e-06,
  "tail_fk_speed_mean_m_s": -1.049034148304073e-05,
  "peak_tilt_rad": 0.055736252267709174,
  "peak_wheel_torque_nm": 0.24574241042137146,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.014062382666135444,
  "final_integral_m_s": 0.01408085416172645,
  "elapsed_wall_s": 16.511458126013167
}
```
