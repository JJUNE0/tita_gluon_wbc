# tita_flash_sac_115632_883848_model_40000_s271

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a4b5c15c3add7114e65d55cabbe505c0fffcd993df1b9162587e073cca97a891

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_40000_s271",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_40000",
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
  "checkpoint_sha256": "a4b5c15c3add7114e65d55cabbe505c0fffcd993df1b9162587e073cca97a891",
  "onnx_sha256": "4722a7e5dc4a1d465689d98943ba5c9a40a7d45a99344f923f067d1cfa90fcb6",
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
  "initial_physics_sha256": "2d096d74441ac7489b4a7057fe8c5a0a39b29b0a8c177f7ef9b1afd89c62fd9c",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.02203697538063924,
  "max_drift_m": 0.04817891685111235,
  "radial_IAE_m_s": 1.3261818923009758,
  "signed_longitudinal_delta_m": 0.022036968372032454,
  "tail_speed_mean_m_s": 5.951588033476568e-06,
  "tail_speed_rms_m_s": 6.004476819115585e-06,
  "tail_sensor_speed_mean_m_s": 5.794228463083206e-06,
  "tail_fk_speed_mean_m_s": 7.99560358732969e-06,
  "peak_tilt_rad": 0.11500564304957028,
  "peak_wheel_torque_nm": 1.170055627822876,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.2376017867149061,
  "final_integral_m_s": 0.2375865523390091,
  "elapsed_wall_s": 4.49488126905635
}
```
