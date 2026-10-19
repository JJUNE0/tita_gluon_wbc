# tita_flash_sac_115632_883848_model_25000_nominal_v01_entry12

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: fd99df31c9e160baa980cd421917f4536bfda16779ad79754dd3d4bf13c600b1

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_25000_nominal_v01_entry12",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_25000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 272,
    "estimator": "fk",
    "physics": {},
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.05,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
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
  "final_drift_m": 0.15345821572623952,
  "max_drift_m": 0.21139644461230128,
  "radial_IAE_m_s": 8.93679695508235,
  "signed_longitudinal_delta_m": 0.15345323656335239,
  "tail_speed_mean_m_s": 0.00014480652636885986,
  "tail_speed_rms_m_s": 0.00014662416528162897,
  "tail_sensor_speed_mean_m_s": 0.00014433561914053243,
  "tail_fk_speed_mean_m_s": 0.00015376479542344074,
  "peak_tilt_rad": 0.13959413295056078,
  "peak_wheel_torque_nm": 1.4978594779968262,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 1.3407300856100683,
  "final_integral_m_s": 1.340506276694762,
  "elapsed_wall_s": 4.173966616974212
}
```
