# tita_flash_sac_115632_883848_model_80000_com_plus5mm_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 80677a4fd403aad22ca310d644998b9b9a686da481d6d95eaf8cc02aa67afadc

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_80000_com_plus5mm_v02_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_80000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "com": 0.005
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
  "initial_physics_sha256": "a70c89cfd2868b985651efc6559f5691ddecefae66af7b93784b6d89c63d0d38",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.08399952649614889,
  "max_drift_m": 0.09785834947542559,
  "radial_IAE_m_s": 4.90530286533202,
  "signed_longitudinal_delta_m": 0.08397135254057872,
  "tail_speed_mean_m_s": 5.762471364500426e-05,
  "tail_speed_rms_m_s": 5.921683285396186e-05,
  "tail_sensor_speed_mean_m_s": 5.733811920344814e-05,
  "tail_fk_speed_mean_m_s": 5.7151072670897846e-05,
  "peak_tilt_rad": 0.08638304595778923,
  "peak_wheel_torque_nm": 0.6469435095787048,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.8539581439106353,
  "final_integral_m_s": 0.8538374531002808,
  "elapsed_wall_s": 15.596847657987382
}
```
