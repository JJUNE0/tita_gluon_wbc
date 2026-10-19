# tita_flash_sac_115632_883848_model_60000_mass1.15_baseline

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_60000_mass1.15_baseline",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_60000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 272,
    "physics": {
      "mass": 1.15
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
  "initial_physics_sha256": "0035c473643c9ac44fca17820f236d495acfe9480e24dd190457dfb5f45dac66",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 5.3326355993050205,
  "max_drift_m": 5.3326355993050205,
  "radial_IAE_m_s": 159.97401541031917,
  "signed_longitudinal_delta_m": -5.321016311860408,
  "tail_speed_mean_m_s": -0.08902462537772832,
  "tail_speed_rms_m_s": 0.08902462982046412,
  "tail_sensor_speed_mean_m_s": -0.08883843684303445,
  "tail_fk_speed_mean_m_s": -0.0888362225055398,
  "peak_tilt_rad": 0.059435097102643386,
  "peak_wheel_torque_nm": 0.08347302675247192,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 5.5499707059934735
}
```
