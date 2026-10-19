# tita_flash_sac_193248_068255_model_50000_com_plus5mm_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 948c108cb4740ede74b9c33fdca02f3a0bc4ae70aeb862e20f90c841243b1087

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_50000_com_plus5mm_baseline_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_50000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "com": 0.005
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
  "initial_physics_sha256": "bcc010bda648289668ac77c949efcbeccfce0dc8cb90abf60e840799e4ddd7b6",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 8.575971766623992,
  "max_drift_m": 8.575971766623992,
  "radial_IAE_m_s": 250.5313362789215,
  "signed_longitudinal_delta_m": 8.57514722659945,
  "tail_speed_mean_m_s": 0.14912715441162983,
  "tail_speed_rms_m_s": 0.14912924371393022,
  "tail_sensor_speed_mean_m_s": 0.14880470944274923,
  "tail_fk_speed_mean_m_s": 0.14880335916528895,
  "peak_tilt_rad": 0.0629512587972163,
  "peak_wheel_torque_nm": 0.29942673444747925,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 6.84279621305177
}
```
