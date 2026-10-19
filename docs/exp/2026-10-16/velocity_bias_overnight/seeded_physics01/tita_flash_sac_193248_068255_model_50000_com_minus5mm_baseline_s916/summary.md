# tita_flash_sac_193248_068255_model_50000_com_minus5mm_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 948c108cb4740ede74b9c33fdca02f3a0bc4ae70aeb862e20f90c841243b1087

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_50000_com_minus5mm_baseline_s916",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_50000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "com": -0.005
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
  "initial_physics_sha256": "645c896a00951229c495c17aefab1c57325abbbf2e709bd7a0c2577d8d0e2258",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 5.504356327507646,
  "max_drift_m": 5.504356327507646,
  "radial_IAE_m_s": 155.52436486587308,
  "signed_longitudinal_delta_m": 5.50433648322245,
  "tail_speed_mean_m_s": 0.10129234083626786,
  "tail_speed_rms_m_s": 0.101301956809942,
  "tail_sensor_speed_mean_m_s": 0.10107370297500297,
  "tail_fk_speed_mean_m_s": 0.10107152710753808,
  "peak_tilt_rad": 0.05339393196926068,
  "peak_wheel_torque_nm": 0.2723093032836914,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 10.398646976973396
}
```
