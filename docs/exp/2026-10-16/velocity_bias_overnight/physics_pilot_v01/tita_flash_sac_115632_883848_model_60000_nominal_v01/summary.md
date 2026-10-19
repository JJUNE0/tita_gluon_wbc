# tita_flash_sac_115632_883848_model_60000_nominal_v01

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_60000_nominal_v01",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_60000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 272,
    "physics": {},
    "kick": 0.0,
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.05,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
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
  "initial_physics_sha256": "eab4665052e291222b718d80b8d936ed47595de36aa169ac480c15a338258055",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.004381306484011929,
  "max_drift_m": 0.006820827823489717,
  "radial_IAE_m_s": 0.2750240803665883,
  "signed_longitudinal_delta_m": 0.0043638179213028,
  "tail_speed_mean_m_s": -9.059674764860299e-06,
  "tail_speed_rms_m_s": 9.367432230381263e-06,
  "tail_sensor_speed_mean_m_s": -9.015139736632563e-06,
  "tail_fk_speed_mean_m_s": -6.9475791241493195e-06,
  "peak_tilt_rad": 0.06933936516677908,
  "peak_wheel_torque_nm": 0.23154225945472717,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.04702411578639669,
  "final_integral_m_s": 0.0470343280392672,
  "elapsed_wall_s": 4.728054516017437
}
```
