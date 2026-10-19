# tita_flash_sac_193248_068255_model_50000_kick+0.2_baseline_s922

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 948c108cb4740ede74b9c33fdca02f3a0bc4ae70aeb862e20f90c841243b1087

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_50000_kick+0.2_baseline_s922",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_50000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 922,
    "estimator": "fk",
    "guarded": false,
    "kick": 0.2,
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
  "initial_physics_sha256": "2298b2a7fc4dc03e00806a7f96e825dc3f7a4776b23e81c9bbe396418c89c3fd",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 7.341637134499977,
  "max_drift_m": 7.341637134499977,
  "radial_IAE_m_s": 217.27717073544156,
  "signed_longitudinal_delta_m": 7.340996020935447,
  "tail_speed_mean_m_s": 0.12669911116504354,
  "tail_speed_rms_m_s": 0.1267031777111773,
  "tail_sensor_speed_mean_m_s": 0.1264253312661932,
  "tail_fk_speed_mean_m_s": 0.12642359143890614,
  "peak_tilt_rad": 0.0797506449399279,
  "peak_wheel_torque_nm": 1.4924678802490234,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 6.057170770014636
}
```
