# tita_flash_sac_115632_883848_model_25000_tau0.2_entry12

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: fd99df31c9e160baa980cd421917f4536bfda16779ad79754dd3d4bf13c600b1

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_25000_tau0.2_entry12",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_25000",
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
  "initial_physics_sha256": "17c8e89bcd920956da58340cfe7614ce3f0d7d132db8607265b0c5ba81c2a0b4",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.15348382679686573,
  "max_drift_m": 0.21896597414410812,
  "radial_IAE_m_s": 8.92644957981571,
  "signed_longitudinal_delta_m": 0.15347590743102513,
  "tail_speed_mean_m_s": 0.00014043479456606043,
  "tail_speed_rms_m_s": 0.00014270312187151913,
  "tail_sensor_speed_mean_m_s": 0.00013969142711378637,
  "tail_fk_speed_mean_m_s": 0.0001490844832533108,
  "peak_tilt_rad": 0.1483341545388288,
  "peak_wheel_torque_nm": 1.3700565099716187,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 1.3423162081138116,
  "final_integral_m_s": 1.3420941586929747,
  "elapsed_wall_s": 6.071091245044954
}
```
