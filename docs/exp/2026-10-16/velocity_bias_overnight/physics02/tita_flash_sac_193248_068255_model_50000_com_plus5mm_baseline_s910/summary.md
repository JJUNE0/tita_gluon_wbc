# tita_flash_sac_193248_068255_model_50000_com_plus5mm_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 948c108cb4740ede74b9c33fdca02f3a0bc4ae70aeb862e20f90c841243b1087

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_50000_com_plus5mm_baseline_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_50000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "com": 0.005
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "948c108cb4740ede74b9c33fdca02f3a0bc4ae70aeb862e20f90c841243b1087",
  "onnx_sha256": "9edc5ad830f2e0f0d88dcb9bd8a21a023d3cdd754ce2e54339650dc66d2bb1c4",
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
  "initial_physics_sha256": "c4f2e5c18c51007811cf608e75906ba958c253f77607156ba16360034bd4683d",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 8.492713703519001,
  "max_drift_m": 8.492713703519001,
  "radial_IAE_m_s": 246.97370047835295,
  "signed_longitudinal_delta_m": 8.49269959820183,
  "tail_speed_mean_m_s": 0.14866187407406845,
  "tail_speed_rms_m_s": 0.148664446416206,
  "tail_sensor_speed_mean_m_s": 0.1483404733891929,
  "tail_fk_speed_mean_m_s": 0.1483391503304604,
  "peak_tilt_rad": 0.06293395692446357,
  "peak_wheel_torque_nm": 0.2978214621543884,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 12.122346561052836
}
```
