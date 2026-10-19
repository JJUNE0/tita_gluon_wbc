# tita_flash_sac_115632_883848_model_25000_kick-0.2_v01

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: fd99df31c9e160baa980cd421917f4536bfda16779ad79754dd3d4bf13c600b1

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_25000_kick-0.2_v01",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_25000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 272,
    "physics": {},
    "kick": -0.2,
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
  "initial_physics_sha256": "ccca7a036642051623ea6854c5e3a1697eb56ccdb85995528da63c1435e97cd4",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.13042698285232437,
  "max_drift_m": 0.1587042025219049,
  "radial_IAE_m_s": 7.622553648317387,
  "signed_longitudinal_delta_m": 0.13041691981908665,
  "tail_speed_mean_m_s": 8.736013900767949e-05,
  "tail_speed_rms_m_s": 8.789097359984301e-05,
  "tail_sensor_speed_mean_m_s": 8.967786928451472e-05,
  "tail_fk_speed_mean_m_s": 0.00010070363003033005,
  "peak_tilt_rad": 0.12604584677822284,
  "peak_wheel_torque_nm": 1.7834701538085938,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 1.3715473957431021,
  "final_integral_m_s": 1.3713748909246861,
  "elapsed_wall_s": 4.807645450986456
}
```
