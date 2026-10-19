# tita_flash_sac_115632_883848_model_65000_kick-0.2_v02_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a28e8551929d9a4412f571a2e91577da75879477c15d61f0774ab6f05354dff3

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_65000_kick-0.2_v02_s912",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_65000",
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
  "initial_physics_sha256": "2e6e46f5ddca23c3e4a29da43d6d5bb75df7d59539cbddcfdfb3766409b46f45",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.0034162204677234105,
  "max_drift_m": 0.057306200641504164,
  "radial_IAE_m_s": 0.2735451394435725,
  "signed_longitudinal_delta_m": 0.0033387451870073768,
  "tail_speed_mean_m_s": -9.062265283109601e-06,
  "tail_speed_rms_m_s": 9.07518229671904e-06,
  "tail_sensor_speed_mean_m_s": -8.844183612874251e-06,
  "tail_fk_speed_mean_m_s": -1.0031968830911117e-05,
  "peak_tilt_rad": 0.11012045488395117,
  "peak_wheel_torque_nm": 1.6523370742797852,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.04986478806047169,
  "final_integral_m_s": 0.049883396797822215,
  "elapsed_wall_s": 16.1467503500171
}
```
