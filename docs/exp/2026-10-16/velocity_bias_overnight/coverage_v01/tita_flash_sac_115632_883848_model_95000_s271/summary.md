# tita_flash_sac_115632_883848_model_95000_s271

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 7fc976ceb0b69090d3baf26399d36e566e21da7bf1a3f935bf0a1bc7b29a5d82

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_95000_s271",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_95000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 271,
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.05,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
    },
    "estimator": "fk"
  },
  "checkpoint_sha256": "7fc976ceb0b69090d3baf26399d36e566e21da7bf1a3f935bf0a1bc7b29a5d82",
  "onnx_sha256": "1a45e6567675d4dfc1a738bbe430e52a4f2a2cab73c2c908c46928d22bd54530",
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
  "initial_physics_sha256": "05d25ff4f3ed3025679fcec7e49c581c5ad3390b24c958bdcf8d98a3a2b06823",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.008854792553404113,
  "max_drift_m": 0.008854792553404113,
  "radial_IAE_m_s": 0.3615982282129817,
  "signed_longitudinal_delta_m": 0.008844954432874799,
  "tail_speed_mean_m_s": 0.00010909678551881802,
  "tail_speed_rms_m_s": 0.00010914433959085664,
  "tail_sensor_speed_mean_m_s": 0.00010880405172484195,
  "tail_fk_speed_mean_m_s": 0.00010939411325963135,
  "peak_tilt_rad": 0.06174259597451193,
  "peak_wheel_torque_nm": 0.18998855352401733,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.09048351550665042,
  "final_integral_m_s": 0.09025514203741097,
  "elapsed_wall_s": 4.333107104001101
}
```
