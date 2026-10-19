# tita_flash_sac_115632_883848_model_75000_baseline_s911_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 381e846e3ffb1d5a9ed629c02b55c9740ec3c5b089ca443f38b3d73b6abbd730

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_75000_baseline_s911_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_75000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 911,
    "estimator": "fk",
    "runtime": false,
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "381e846e3ffb1d5a9ed629c02b55c9740ec3c5b089ca443f38b3d73b6abbd730",
  "onnx_sha256": "2bd3f78d10bc3b7cc4e50272d0289147f13b0a62ac6730048ba653ae53f35114",
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
  "initial_physics_sha256": "4f1f929c80d99b2164b11a2cd1cefa8dbb02b836a50a9ec199f5e0ab21f7c061",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 2.011530106559362,
  "max_drift_m": 2.011530106559362,
  "radial_IAE_m_s": 176.4577276965119,
  "signed_longitudinal_delta_m": 2.0025200647372188,
  "tail_speed_mean_m_s": 0.014418645623757527,
  "tail_speed_rms_m_s": 0.014420709531172029,
  "tail_sensor_speed_mean_m_s": 0.01438762055388634,
  "tail_fk_speed_mean_m_s": 0.01438761241220023,
  "peak_tilt_rad": 0.053453675483503105,
  "peak_wheel_torque_nm": 0.1564244031906128,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 53.106777614040766
}
```
