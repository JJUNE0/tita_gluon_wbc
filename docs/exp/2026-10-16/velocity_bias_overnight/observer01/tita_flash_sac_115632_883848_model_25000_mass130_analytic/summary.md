# tita_flash_sac_115632_883848_model_25000_mass130_analytic

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: fd99df31c9e160baa980cd421917f4536bfda16779ad79754dd3d4bf13c600b1

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_25000_mass130_analytic",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_25000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 272,
    "estimator": "analytic",
    "physics": {
      "mass": 1.3
    },
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.1,
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
  "initial_physics_sha256": "f2abcc0ff3c285cec9bdaca65a03d7f4844531bf6f4e8f1a3cf42f588b88824d",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.01698957979695263,
  "max_drift_m": 0.03339904796771865,
  "radial_IAE_m_s": 1.0233470608120336,
  "signed_longitudinal_delta_m": 0.01696497644268076,
  "tail_speed_mean_m_s": -5.50159965549515e-07,
  "tail_speed_rms_m_s": 1.264528172292413e-06,
  "tail_sensor_speed_mean_m_s": -6.06618303475029e-07,
  "tail_fk_speed_mean_m_s": -1.2747907097328863e-08,
  "peak_tilt_rad": 0.11172830356245256,
  "peak_wheel_torque_nm": 1.3404579162597656,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.1812754867130734,
  "final_integral_m_s": 0.18127858143605743,
  "elapsed_wall_s": 18.071219455974642
}
```
