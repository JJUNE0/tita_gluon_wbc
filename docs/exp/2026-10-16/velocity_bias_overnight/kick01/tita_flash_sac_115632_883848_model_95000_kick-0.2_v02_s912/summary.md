# tita_flash_sac_115632_883848_model_95000_kick-0.2_v02_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 7fc976ceb0b69090d3baf26399d36e566e21da7bf1a3f935bf0a1bc7b29a5d82

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_95000_kick-0.2_v02_s912",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_95000",
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
  "checkpoint_sha256": "7fc976ceb0b69090d3baf26399d36e566e21da7bf1a3f935bf0a1bc7b29a5d82",
  "onnx_sha256": "1a45e6567675d4dfc1a738bbe430e52a4f2a2cab73c2c908c46928d22bd54530",
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
  "initial_physics_sha256": "408bb601abda4270c007aaee7b68440239b73bfff8e9996e7cb94a3c9f1b3330",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.0070624746892728515,
  "max_drift_m": 0.097084721813284,
  "radial_IAE_m_s": 0.39386766183583877,
  "signed_longitudinal_delta_m": 0.006971695547148229,
  "tail_speed_mean_m_s": 9.835514394291746e-05,
  "tail_speed_rms_m_s": 9.935704022210325e-05,
  "tail_sensor_speed_mean_m_s": 9.806350639358872e-05,
  "tail_fk_speed_mean_m_s": 9.866284240150089e-05,
  "peak_tilt_rad": 0.12015011556511301,
  "peak_wheel_torque_nm": 1.8557933568954468,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0817606034600178,
  "final_integral_m_s": 0.08154486016189404,
  "elapsed_wall_s": 18.967013626999687
}
```
