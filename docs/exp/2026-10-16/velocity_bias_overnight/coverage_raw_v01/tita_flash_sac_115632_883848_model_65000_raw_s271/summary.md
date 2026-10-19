# tita_flash_sac_115632_883848_model_65000_raw_s271

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a28e8551929d9a4412f571a2e91577da75879477c15d61f0774ab6f05354dff3

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_65000_raw_s271",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_65000",
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
  "initial_physics_sha256": "c2839aafb313699ba202dbf93e016fa3daf89d465cb718fd717575381d8b5396",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.0030253974248514053,
  "max_drift_m": 0.01117584549328815,
  "radial_IAE_m_s": 0.2960426901131936,
  "signed_longitudinal_delta_m": 0.0030176918850581555,
  "tail_speed_mean_m_s": -9.025055942592449e-05,
  "tail_speed_rms_m_s": 0.008322710620773478,
  "tail_sensor_speed_mean_m_s": -0.00039324155680881245,
  "tail_fk_speed_mean_m_s": -5.140222595442218e-05,
  "peak_tilt_rad": 0.06025389482778154,
  "peak_wheel_torque_nm": 1.2100932598114014,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.1341381434902753,
  "final_integral_m_s": 0.011166288941111435,
  "elapsed_wall_s": 4.428018030012026
}
```
