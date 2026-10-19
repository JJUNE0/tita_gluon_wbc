# tita_flash_sac_115632_883848_model_65000_kick+0.2_v02_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a28e8551929d9a4412f571a2e91577da75879477c15d61f0774ab6f05354dff3

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_65000_kick+0.2_v02_s912",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_65000",
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
  "checkpoint_sha256": "a28e8551929d9a4412f571a2e91577da75879477c15d61f0774ab6f05354dff3",
  "onnx_sha256": "7cc289e8aee44513f1e29487c7522e96c762174e2444aedaa7aea78b3a66a3ec",
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
  "initial_physics_sha256": "e6bb68f059323e1c520a739dc868454afe993065f21234e681b4c3db270dc174",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.006019251463964022,
  "max_drift_m": 0.08363647098669294,
  "radial_IAE_m_s": 0.44815381486256745,
  "signed_longitudinal_delta_m": 0.006008827535711116,
  "tail_speed_mean_m_s": -8.804623029463196e-06,
  "tail_speed_rms_m_s": 8.817465479212353e-06,
  "tail_sensor_speed_mean_m_s": -8.608288998721289e-06,
  "tail_fk_speed_mean_m_s": -9.79865228704006e-06,
  "peak_tilt_rad": 0.07959926095075875,
  "peak_wheel_torque_nm": 1.6723709106445312,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.04957826395746146,
  "final_integral_m_s": 0.049596478863596326,
  "elapsed_wall_s": 14.156340997025836
}
```
