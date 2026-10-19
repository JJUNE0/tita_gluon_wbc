# tita_flash_sac_193248_068255_model_50000_mass130_v03_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 948c108cb4740ede74b9c33fdca02f3a0bc4ae70aeb862e20f90c841243b1087

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_50000_mass130_v03_s916",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_50000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "mass": 1.3
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
  "checkpoint_sha256": "948c108cb4740ede74b9c33fdca02f3a0bc4ae70aeb862e20f90c841243b1087",
  "onnx_sha256": "9edc5ad830f2e0f0d88dcb9bd8a21a023d3cdd754ce2e54339650dc66d2bb1c4",
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
  "initial_physics_sha256": "5147c1052e6ef02040fe7e859455ff4104e9e06f69e7560bf335df38e77ebe0d",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.1026851476138903,
  "max_drift_m": 0.1029724193787529,
  "radial_IAE_m_s": 4.118611089859689,
  "signed_longitudinal_delta_m": -0.09992648341252115,
  "tail_speed_mean_m_s": -0.0015386997082748994,
  "tail_speed_rms_m_s": 0.04362255163740078,
  "tail_sensor_speed_mean_m_s": -0.003912540686835096,
  "tail_fk_speed_mean_m_s": -4.735214657857056e-05,
  "peak_tilt_rad": 0.15241784315941498,
  "peak_wheel_torque_nm": 8.20132827758789,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.049560925143209464,
  "final_integral_m_s": -0.049560925143209464,
  "elapsed_wall_s": 11.124140102008823
}
```
