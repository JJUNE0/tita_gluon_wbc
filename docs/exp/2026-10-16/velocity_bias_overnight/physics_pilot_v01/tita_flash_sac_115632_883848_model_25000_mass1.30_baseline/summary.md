# tita_flash_sac_115632_883848_model_25000_mass1.30_baseline

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: fd99df31c9e160baa980cd421917f4536bfda16779ad79754dd3d4bf13c600b1

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_25000_mass1.30_baseline",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_25000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 272,
    "physics": {
      "mass": 1.3
    },
    "kick": 0.0,
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "estimator": "fk"
  },
  "checkpoint_sha256": "fd99df31c9e160baa980cd421917f4536bfda16779ad79754dd3d4bf13c600b1",
  "onnx_sha256": "494320c9b871a706a00e8f350ff196243c37e61c0d12ed2ab0503ea24d273b8f",
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
  "initial_physics_sha256": "f2abcc0ff3c285cec9bdaca65a03d7f4844531bf6f4e8f1a3cf42f588b88824d",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 5.521968011214033,
  "max_drift_m": 5.521968011214033,
  "radial_IAE_m_s": 165.9066907185807,
  "signed_longitudinal_delta_m": 5.512812849095813,
  "tail_speed_mean_m_s": 0.091878294176488,
  "tail_speed_rms_m_s": 0.09187830509152471,
  "tail_sensor_speed_mean_m_s": 0.0916809042122051,
  "tail_fk_speed_mean_m_s": 0.09167886017728383,
  "peak_tilt_rad": 0.11175587573685641,
  "peak_wheel_torque_nm": 0.017603576183319092,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 5.395094626001082
}
```
