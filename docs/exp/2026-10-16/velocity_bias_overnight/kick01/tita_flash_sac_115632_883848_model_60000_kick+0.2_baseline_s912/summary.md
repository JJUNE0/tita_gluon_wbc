# tita_flash_sac_115632_883848_model_60000_kick+0.2_baseline_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_60000_kick+0.2_baseline_s912",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_60000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 912,
    "estimator": "fk",
    "runtime": false,
    "kick": 0.2,
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
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
  "initial_physics_sha256": "3ed1b14ef0116d572f2266cc6a9a69aec0aee5b2b240da5d1e531e12d2101a13",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 1.070977976253141,
  "max_drift_m": 1.070977976253141,
  "radial_IAE_m_s": 36.16271690885078,
  "signed_longitudinal_delta_m": 1.0702403399064206,
  "tail_speed_mean_m_s": 0.01584270130695091,
  "tail_speed_rms_m_s": 0.015844593312641483,
  "tail_sensor_speed_mean_m_s": 0.015808408000665543,
  "tail_fk_speed_mean_m_s": 0.015809844661366715,
  "peak_tilt_rad": 0.09691463387180232,
  "peak_wheel_torque_nm": 1.7559738159179688,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 11.097064854984637
}
```
