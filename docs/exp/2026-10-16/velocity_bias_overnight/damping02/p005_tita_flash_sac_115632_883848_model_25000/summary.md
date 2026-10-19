# p005_tita_flash_sac_115632_883848_model_25000

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: fd99df31c9e160baa980cd421917f4536bfda16779ad79754dd3d4bf13c600b1

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "p005_tita_flash_sac_115632_883848_model_25000",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_25000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "analytic",
    "physics": {},
    "law": {
      "kp": 2.0,
      "ki": 15.0,
      "tau": 0.15,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0,
      "kp_fast": 3.0
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
  "initial_physics_sha256": "6a7623095d59b3790ae881c3fb20f5d23e46e39e8f7925b4c03378dac73ab1e4",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.2211621539287117,
  "max_drift_m": 0.25663020471317716,
  "radial_IAE_m_s": 12.854675533465723,
  "signed_longitudinal_delta_m": 0.22113444506391114,
  "tail_speed_mean_m_s": 7.019831518479324e-05,
  "tail_speed_rms_m_s": 7.124275248396958e-05,
  "tail_sensor_speed_mean_m_s": 6.895743586563384e-05,
  "tail_fk_speed_mean_m_s": 7.81034821561632e-05,
  "peak_tilt_rad": 0.14351632415034898,
  "peak_wheel_torque_nm": 1.6719977855682373,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 1.3536509400621717,
  "final_integral_m_s": 1.353507828759856,
  "elapsed_wall_s": 12.828700023004785
}
```
