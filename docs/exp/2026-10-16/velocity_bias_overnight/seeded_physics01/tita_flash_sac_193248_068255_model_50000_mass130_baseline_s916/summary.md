# tita_flash_sac_193248_068255_model_50000_mass130_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 948c108cb4740ede74b9c33fdca02f3a0bc4ae70aeb862e20f90c841243b1087

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_50000_mass130_baseline_s916",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_50000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "mass": 1.3
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
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
  "final_drift_m": 0.8198914502755641,
  "max_drift_m": 0.8198914502755641,
  "radial_IAE_m_s": 24.73224657093804,
  "signed_longitudinal_delta_m": -0.7791509183275291,
  "tail_speed_mean_m_s": -0.014065859133457587,
  "tail_speed_rms_m_s": 0.04485423349932085,
  "tail_sensor_speed_mean_m_s": -0.017442907678481664,
  "tail_fk_speed_mean_m_s": -0.013168113267386266,
  "peak_tilt_rad": 0.14552184584361116,
  "peak_wheel_torque_nm": 8.030643463134766,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 10.882990199956112
}
```
