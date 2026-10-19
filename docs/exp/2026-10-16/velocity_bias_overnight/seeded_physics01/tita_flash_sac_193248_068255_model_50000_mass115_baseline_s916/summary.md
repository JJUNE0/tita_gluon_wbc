# tita_flash_sac_193248_068255_model_50000_mass115_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 948c108cb4740ede74b9c33fdca02f3a0bc4ae70aeb862e20f90c841243b1087

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_50000_mass115_baseline_s916",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_50000",
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
  "initial_physics_sha256": "2c44175c2f97f71a9c74b5ed3778b45c62787c717a60d7c7cd579b20f5f6e90e",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 1.2545993809274436,
  "max_drift_m": 1.2545993809274436,
  "radial_IAE_m_s": 36.17455268292849,
  "signed_longitudinal_delta_m": 1.2517177153786863,
  "tail_speed_mean_m_s": 0.02220470869137813,
  "tail_speed_rms_m_s": 0.0268641831366733,
  "tail_sensor_speed_mean_m_s": 0.022339835092668868,
  "tail_fk_speed_mean_m_s": 0.022598866492310583,
  "peak_tilt_rad": 0.08750489817598739,
  "peak_wheel_torque_nm": 5.424233436584473,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 10.423873396008275
}
```
