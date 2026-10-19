# p006_tita_flash_sac_115632_883848_model_25000_kick+0.2

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: fd99df31c9e160baa980cd421917f4536bfda16779ad79754dd3d4bf13c600b1

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "p006_tita_flash_sac_115632_883848_model_25000_kick+0.2",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_25000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 917,
    "estimator": "fk",
    "guarded": true,
    "physics": {},
    "kick": 0.2,
    "law": {
      "kp": 0.0,
      "ki": 4.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 1.0,
      "seed_gain": 3.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
  },
  "checkpoint_sha256": "fd99df31c9e160baa980cd421917f4536bfda16779ad79754dd3d4bf13c600b1",
  "onnx_sha256": "494320c9b871a706a00e8f350ff196243c37e61c0d12ed2ab0503ea24d273b8f",
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
  "initial_physics_sha256": "5295976788d620026a502acbf3646d5d6dd247dafd261219331bf4178a743342",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.21047124638886416,
  "max_drift_m": 0.37707292124306,
  "radial_IAE_m_s": 12.151541595597829,
  "signed_longitudinal_delta_m": 0.21046699276239175,
  "tail_speed_mean_m_s": 0.00035471507719716773,
  "tail_speed_rms_m_s": 0.0003608488841360314,
  "tail_sensor_speed_mean_m_s": 0.00035316918890627015,
  "tail_fk_speed_mean_m_s": 0.00036248836992119166,
  "peak_tilt_rad": 0.16362540029077421,
  "peak_wheel_torque_nm": 3.738144874572754,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 1.3437170350556555,
  "final_integral_m_s": 1.3437170350556555,
  "elapsed_wall_s": 11.138110747968312
}
```
