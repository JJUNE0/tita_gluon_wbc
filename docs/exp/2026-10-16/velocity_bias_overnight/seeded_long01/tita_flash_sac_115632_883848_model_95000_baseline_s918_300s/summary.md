# tita_flash_sac_115632_883848_model_95000_baseline_s918_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 7fc976ceb0b69090d3baf26399d36e566e21da7bf1a3f935bf0a1bc7b29a5d82

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_95000_baseline_s918_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_95000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 918,
    "estimator": "fk",
    "guarded": false,
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
  },
  "checkpoint_sha256": "7fc976ceb0b69090d3baf26399d36e566e21da7bf1a3f935bf0a1bc7b29a5d82",
  "onnx_sha256": "1a45e6567675d4dfc1a738bbe430e52a4f2a2cab73c2c908c46928d22bd54530",
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
  "initial_physics_sha256": "89159ca90fa9f99546805a42ac7da1a297e97bf7ce785af8c3aaefc0ef4910ba",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 11.29376149867963,
  "max_drift_m": 11.29376149867963,
  "radial_IAE_m_s": 1420.9050763261764,
  "signed_longitudinal_delta_m": 11.118559039716983,
  "tail_speed_mean_m_s": 0.048573600550872315,
  "tail_speed_rms_m_s": 0.048573657853404666,
  "tail_sensor_speed_mean_m_s": 0.04846887600736199,
  "tail_fk_speed_mean_m_s": 0.048469164989844986,
  "peak_tilt_rad": 0.06707689254731064,
  "peak_wheel_torque_nm": 0.18541862070560455,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 44.1577116639819
}
```
