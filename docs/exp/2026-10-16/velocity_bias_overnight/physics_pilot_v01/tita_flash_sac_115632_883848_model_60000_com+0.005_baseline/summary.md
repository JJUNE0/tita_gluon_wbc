# tita_flash_sac_115632_883848_model_60000_com+0.005_baseline

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_60000_com+0.005_baseline",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_60000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 272,
    "physics": {
      "com": 0.005
    },
    "kick": 0.0,
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "estimator": "fk"
  },
  "checkpoint_sha256": "6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05",
  "onnx_sha256": "f44f07ed44970e3ff565eae67fd9229adf0be5c02215591c52a691ffcbb71b2a",
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
  "initial_physics_sha256": "ed96dabaa6d0f84f3e2c60b67d4eebb764890247d7b3f59296b7b7d3987c1f06",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 2.0064042711075207,
  "max_drift_m": 2.0064042711075207,
  "radial_IAE_m_s": 59.7322540564174,
  "signed_longitudinal_delta_m": 2.0056904117966585,
  "tail_speed_mean_m_s": 0.03377506793193307,
  "tail_speed_rms_m_s": 0.03377538289484426,
  "tail_sensor_speed_mean_m_s": 0.03370204013594803,
  "tail_fk_speed_mean_m_s": 0.03370303106754581,
  "peak_tilt_rad": 0.07266586920209628,
  "peak_wheel_torque_nm": 0.12772423028945923,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 5.358316196012311
}
```
