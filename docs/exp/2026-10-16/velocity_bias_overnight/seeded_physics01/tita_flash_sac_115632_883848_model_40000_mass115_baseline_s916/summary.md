# tita_flash_sac_115632_883848_model_40000_mass115_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a4b5c15c3add7114e65d55cabbe505c0fffcd993df1b9162587e073cca97a891

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_40000_mass115_baseline_s916",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_40000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "mass": 1.15
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
  },
  "checkpoint_sha256": "a4b5c15c3add7114e65d55cabbe505c0fffcd993df1b9162587e073cca97a891",
  "onnx_sha256": "4722a7e5dc4a1d465689d98943ba5c9a40a7d45a99344f923f067d1cfa90fcb6",
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
  "initial_physics_sha256": "92f0a7761bba368e2a0b75203122b3d174a375fe5b1b9a60a22d2e5bbcac60db",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 1.0912578284721774,
  "max_drift_m": 1.0912578284721774,
  "radial_IAE_m_s": 32.47111989821533,
  "signed_longitudinal_delta_m": -1.0898195025345747,
  "tail_speed_mean_m_s": -0.018496813137856984,
  "tail_speed_rms_m_s": 0.018497016083521677,
  "tail_sensor_speed_mean_m_s": -0.018457179096686174,
  "tail_fk_speed_mean_m_s": -0.01845669691588096,
  "peak_tilt_rad": 0.09753869733992171,
  "peak_wheel_torque_nm": 0.2679702043533325,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 16.177481963008177
}
```
