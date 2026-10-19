# tita_flash_sac_115632_883848_model_25000_raw_s271

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: fd99df31c9e160baa980cd421917f4536bfda16779ad79754dd3d4bf13c600b1

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_25000_raw_s271",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_25000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 271,
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.05,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
    },
    "estimator": "raw"
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
  "initial_physics_sha256": "5a40b7c8376ec83c59a713537e6572d5e2c9491454a451f151ec6a3fa4441570",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.2022890080361627,
  "max_drift_m": 0.2355394876041258,
  "radial_IAE_m_s": 11.898053468336178,
  "signed_longitudinal_delta_m": 0.2022792179979802,
  "tail_speed_mean_m_s": 9.786019479703754e-05,
  "tail_speed_rms_m_s": 9.828896311454717e-05,
  "tail_sensor_speed_mean_m_s": 0.00010025159394702763,
  "tail_fk_speed_mean_m_s": 0.0001113196928551321,
  "peak_tilt_rad": 0.13060456960704658,
  "peak_wheel_torque_nm": 1.6199942827224731,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 1.3718248846896075,
  "final_integral_m_s": 1.3716530610355304,
  "elapsed_wall_s": 4.5396673629875295
}
```
