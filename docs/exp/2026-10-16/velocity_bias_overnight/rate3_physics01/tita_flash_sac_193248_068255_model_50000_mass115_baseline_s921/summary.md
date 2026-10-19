# tita_flash_sac_193248_068255_model_50000_mass115_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 948c108cb4740ede74b9c33fdca02f3a0bc4ae70aeb862e20f90c841243b1087

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_50000_mass115_baseline_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_50000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "mass": 1.15
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
  "initial_physics_sha256": "2855f36cbb78a6aa2645823863b680e968433d754d27a8b1dc6e35235ecc0163",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 1.254599904897707,
  "max_drift_m": 1.254599904897707,
  "radial_IAE_m_s": 36.17459698754438,
  "signed_longitudinal_delta_m": 1.251718243417332,
  "tail_speed_mean_m_s": 0.02220467328430674,
  "tail_speed_rms_m_s": 0.026864128675923478,
  "tail_sensor_speed_mean_m_s": 0.0223398014406256,
  "tail_fk_speed_mean_m_s": 0.022598824598339545,
  "peak_tilt_rad": 0.08750472734113868,
  "peak_wheel_torque_nm": 5.424203872680664,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.964355911011808
}
```
