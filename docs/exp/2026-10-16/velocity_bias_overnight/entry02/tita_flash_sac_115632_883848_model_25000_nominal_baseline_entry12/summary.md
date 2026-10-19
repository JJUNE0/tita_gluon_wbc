# tita_flash_sac_115632_883848_model_25000_nominal_baseline_entry12

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: fd99df31c9e160baa980cd421917f4536bfda16779ad79754dd3d4bf13c600b1

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_25000_nominal_baseline_entry12",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_25000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 272,
    "estimator": "fk",
    "physics": {},
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
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
  "initial_physics_sha256": "857d89af089d95e750e171133cfda9aec3d378e331068c15d9d18be2e1d0409a",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 22.04387673446994,
  "max_drift_m": 22.04387673446994,
  "radial_IAE_m_s": 667.0145921294494,
  "signed_longitudinal_delta_m": 21.421089666190362,
  "tail_speed_mean_m_s": 0.3736941774519986,
  "tail_speed_rms_m_s": 0.37370351028648136,
  "tail_sensor_speed_mean_m_s": 0.37291156458244823,
  "tail_fk_speed_mean_m_s": 0.3728992394945588,
  "peak_tilt_rad": 0.14035626038650206,
  "peak_wheel_torque_nm": 1.1433143615722656,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 4.249417719023768
}
```
