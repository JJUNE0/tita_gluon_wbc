# p001_tita_flash_sac_115632_883848_model_25000_kick+0.0

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: fd99df31c9e160baa980cd421917f4536bfda16779ad79754dd3d4bf13c600b1

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "p001_tita_flash_sac_115632_883848_model_25000_kick+0.0",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_25000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 915,
    "estimator": "fk",
    "guarded": true,
    "physics": {},
    "kick": 0.0,
    "law": {
      "kp": 0.0,
      "ki": 4.0,
      "tau": 0.1,
      "ramp": 0.05,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0,
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
  "initial_physics_sha256": "733b4ac62990505761996234d6b7680d713421f07c1b91361c63e66f9f1853d2",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.09348106257943044,
  "max_drift_m": 0.20450987576880775,
  "radial_IAE_m_s": 5.054424727493807,
  "signed_longitudinal_delta_m": 0.09347835494408109,
  "tail_speed_mean_m_s": 0.0003511277789264819,
  "tail_speed_rms_m_s": 0.0003574998714925341,
  "tail_sensor_speed_mean_m_s": 0.00034951060637652124,
  "tail_fk_speed_mean_m_s": 0.00035882185517470145,
  "peak_tilt_rad": 0.1395625392580786,
  "peak_wheel_torque_nm": 1.6315264701843262,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 1.3442968780031102,
  "final_integral_m_s": 1.3442968780031102,
  "elapsed_wall_s": 12.862230788974557
}
```
