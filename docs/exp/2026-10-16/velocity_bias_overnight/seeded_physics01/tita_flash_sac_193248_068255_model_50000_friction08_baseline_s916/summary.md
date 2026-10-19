# tita_flash_sac_193248_068255_model_50000_friction08_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 948c108cb4740ede74b9c33fdca02f3a0bc4ae70aeb862e20f90c841243b1087

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_50000_friction08_baseline_s916",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_50000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "friction": 0.8
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
  "initial_physics_sha256": "98ab644b3d56a7b57801d1de00caa63442ce5868cb967fe81837256d7d8dc0de",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 6.943236226567679,
  "max_drift_m": 6.943236226567679,
  "radial_IAE_m_s": 197.7510081464093,
  "signed_longitudinal_delta_m": 6.940386460167341,
  "tail_speed_mean_m_s": 0.12538453609948155,
  "tail_speed_rms_m_s": 0.12539028786521444,
  "tail_sensor_speed_mean_m_s": 0.1251135777633533,
  "tail_fk_speed_mean_m_s": 0.12511194518964597,
  "peak_tilt_rad": 0.058365055939332056,
  "peak_wheel_torque_nm": 0.2602469027042389,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 10.224622079986148
}
```
