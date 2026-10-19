# tita_flash_sac_115632_883848_model_80000_kick+0.2_v02_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 80677a4fd403aad22ca310d644998b9b9a686da481d6d95eaf8cc02aa67afadc

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_80000_kick+0.2_v02_s912",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_80000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 912,
    "estimator": "fk",
    "runtime": true,
    "kick": 0.2,
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
  "initial_physics_sha256": "a79c1c5fb51168252df809df24ae1949a8e29b5b826ffc6aea88e9c9e0415f54",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.08227518600379646,
  "max_drift_m": 0.17397274392912995,
  "radial_IAE_m_s": 4.820092223577962,
  "signed_longitudinal_delta_m": 0.0822297779688184,
  "tail_speed_mean_m_s": 5.2959645610020806e-05,
  "tail_speed_rms_m_s": 5.462998277825661e-05,
  "tail_sensor_speed_mean_m_s": 5.265897944645952e-05,
  "tail_fk_speed_mean_m_s": 5.30177903575304e-05,
  "peak_tilt_rad": 0.1564565394227837,
  "peak_wheel_torque_nm": 2.1345789432525635,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.8259777936949716,
  "final_integral_m_s": 0.825870484236977,
  "elapsed_wall_s": 21.776727630000096
}
```
