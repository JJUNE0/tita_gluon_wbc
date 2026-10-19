# tita_flash_sac_115632_883848_model_60000_seeded_v03_s915

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_60000_seeded_v03_s915",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_60000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 915,
    "estimator": "fk",
    "guarded": true,
    "law": {
      "kp": 0.0,
      "ki": 4.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0,
      "seed_gain": 3.0
    },
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
  },
  "checkpoint_sha256": "6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05",
  "onnx_sha256": "f44f07ed44970e3ff565eae67fd9229adf0be5c02215591c52a691ffcbb71b2a",
  "input_columns": [
    "velocity_bias_m_s",
    "filtered_velocity_m_s",
    "integral_m_s"
  ],
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
  "initial_physics_sha256": "b368a4c5d57079fecbed7746582aa3bf18c932345ef9c858891544d04d51c4f1",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.002432503569634565,
  "max_drift_m": 0.00787421021452013,
  "radial_IAE_m_s": 0.17237426794515318,
  "signed_longitudinal_delta_m": 0.0024066714628564745,
  "tail_speed_mean_m_s": -2.0606329288913728e-05,
  "tail_speed_rms_m_s": 2.1523990865712286e-05,
  "tail_sensor_speed_mean_m_s": -2.0549258746308666e-05,
  "tail_fk_speed_mean_m_s": -1.847809158823655e-05,
  "peak_tilt_rad": 0.06903178416639832,
  "peak_wheel_torque_nm": 0.19183632731437683,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.04710482812309021,
  "final_integral_m_s": 0.04710482812309021,
  "elapsed_wall_s": 4.5807316909777
}
```
