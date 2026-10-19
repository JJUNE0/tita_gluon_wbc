# tita_flash_sac_193248_068255_model_50000_friction08_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 948c108cb4740ede74b9c33fdca02f3a0bc4ae70aeb862e20f90c841243b1087

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_50000_friction08_baseline_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_50000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "friction": 0.8
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
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
  "initial_physics_sha256": "615e29a4ca3f07f7d014ff1b03d358b9d525e51766fdd408a62e5dd285e9de71",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 6.943236577928103,
  "max_drift_m": 6.943236577928103,
  "radial_IAE_m_s": 197.75101976410943,
  "signed_longitudinal_delta_m": 6.940386811394419,
  "tail_speed_mean_m_s": 0.12538453899014446,
  "tail_speed_rms_m_s": 0.125390290739414,
  "tail_sensor_speed_mean_m_s": 0.12511358252191015,
  "tail_fk_speed_mean_m_s": 0.12511194851777646,
  "peak_tilt_rad": 0.0583651350870662,
  "peak_wheel_torque_nm": 0.26023972034454346,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 8.39185387903126
}
```
