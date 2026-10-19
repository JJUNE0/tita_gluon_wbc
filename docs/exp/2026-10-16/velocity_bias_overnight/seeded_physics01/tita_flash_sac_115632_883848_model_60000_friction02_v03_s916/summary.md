# tita_flash_sac_115632_883848_model_60000_friction02_v03_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_60000_friction02_v03_s916",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_60000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "friction": 0.2
    },
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
  "initial_physics_sha256": "deed6babf63b55659cff5d1c5586fed747093b46825a469b77c1c6dd8ba17feb",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.004216102399816572,
  "max_drift_m": 0.0076848385015541735,
  "radial_IAE_m_s": 0.20923947370634455,
  "signed_longitudinal_delta_m": -0.004188385864659032,
  "tail_speed_mean_m_s": 5.748564767337487e-07,
  "tail_speed_rms_m_s": 5.859746099167455e-07,
  "tail_sensor_speed_mean_m_s": -3.4784038679210325e-05,
  "tail_fk_speed_mean_m_s": -1.607436769514231e-07,
  "peak_tilt_rad": 0.06149664655691023,
  "peak_wheel_torque_nm": 0.17789717018604279,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.04234308479727026,
  "final_integral_m_s": 0.04234308479727026,
  "elapsed_wall_s": 11.610688039043453
}
```
