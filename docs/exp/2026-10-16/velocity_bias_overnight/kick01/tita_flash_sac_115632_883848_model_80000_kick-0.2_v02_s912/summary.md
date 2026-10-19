# tita_flash_sac_115632_883848_model_80000_kick-0.2_v02_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 80677a4fd403aad22ca310d644998b9b9a686da481d6d95eaf8cc02aa67afadc

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_80000_kick-0.2_v02_s912",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_80000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 912,
    "estimator": "fk",
    "runtime": true,
    "kick": -0.2,
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
  "checkpoint_sha256": "80677a4fd403aad22ca310d644998b9b9a686da481d6d95eaf8cc02aa67afadc",
  "onnx_sha256": "c7a83d6c9814cc6aa8357e4b0215d65d880dd6b756de2de920967396e901c93b",
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
  "initial_physics_sha256": "cfb5cd7764d3c98b50075737046bc85b54d0ad27c395b53026211398f9f76285",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.079300246266551,
  "max_drift_m": 0.08422095907649699,
  "radial_IAE_m_s": 4.574495022488681,
  "signed_longitudinal_delta_m": 0.07924617220005424,
  "tail_speed_mean_m_s": 5.183602370358154e-05,
  "tail_speed_rms_m_s": 5.42506165528066e-05,
  "tail_sensor_speed_mean_m_s": 5.162667496247225e-05,
  "tail_fk_speed_mean_m_s": 5.1904908921928014e-05,
  "peak_tilt_rad": 0.08803305067583667,
  "peak_wheel_torque_nm": 2.0098555088043213,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.8209017548522786,
  "final_integral_m_s": 0.8207928747810812,
  "elapsed_wall_s": 22.39845693600364
}
```
