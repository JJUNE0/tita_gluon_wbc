# tita_flash_sac_115632_883848_model_60000_kick-0.2_baseline

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_60000_kick-0.2_baseline",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_60000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 272,
    "physics": {},
    "kick": -0.2,
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
  "initial_physics_sha256": "df8708d5018c3eb5125efcea8a4cb8e184b4797e4a597d32d2a35df4de4b7166",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.7756666610702383,
  "max_drift_m": 0.7756666610702383,
  "radial_IAE_m_s": 19.806144733592127,
  "signed_longitudinal_delta_m": 0.7749595721171617,
  "tail_speed_mean_m_s": 0.01595701493561921,
  "tail_speed_rms_m_s": 0.015958911008762268,
  "tail_sensor_speed_mean_m_s": 0.015922584142593378,
  "tail_fk_speed_mean_m_s": 0.015923939508947403,
  "peak_tilt_rad": 0.06933936516677908,
  "peak_wheel_torque_nm": 1.588348388671875,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 4.654451053007506
}
```
