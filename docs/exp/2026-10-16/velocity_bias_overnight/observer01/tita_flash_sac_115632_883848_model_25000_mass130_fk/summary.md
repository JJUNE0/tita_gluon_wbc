# tita_flash_sac_115632_883848_model_25000_mass130_fk

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: fd99df31c9e160baa980cd421917f4536bfda16779ad79754dd3d4bf13c600b1

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_25000_mass130_fk",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_25000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 272,
    "estimator": "fk",
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
  "final_drift_m": 0.016893946143939447,
  "max_drift_m": 0.03329996942038898,
  "radial_IAE_m_s": 1.01782844368899,
  "signed_longitudinal_delta_m": 0.016869197689256526,
  "tail_speed_mean_m_s": -6.062166100451357e-07,
  "tail_speed_rms_m_s": 1.2829385543020434e-06,
  "tail_sensor_speed_mean_m_s": -6.618522793206571e-07,
  "tail_fk_speed_mean_m_s": -1.650994594689741e-08,
  "peak_tilt_rad": 0.11172830339237305,
  "peak_wheel_torque_nm": 1.3949873447418213,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.18127537350262013,
  "final_integral_m_s": 0.18127838496474422,
  "elapsed_wall_s": 13.681344848999288
}
```
