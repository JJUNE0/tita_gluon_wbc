# tita_flash_sac_193248_068255_model_50000_mass130_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 948c108cb4740ede74b9c33fdca02f3a0bc4ae70aeb862e20f90c841243b1087

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_50000_mass130_v04_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_50000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
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
      "slew": 3.0,
      "seed_gain": 3.0
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
  "initial_physics_sha256": "fc5214d0141290ca0adf399c7a24cacaee0073619b452a880f86675b8011c93e",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.10268652801501664,
  "max_drift_m": 0.10297932473685797,
  "radial_IAE_m_s": 4.1187552525158795,
  "signed_longitudinal_delta_m": -0.09992689783653626,
  "tail_speed_mean_m_s": -0.0015396522860405746,
  "tail_speed_rms_m_s": 0.043623937054753745,
  "tail_sensor_speed_mean_m_s": -0.003919205388910078,
  "tail_fk_speed_mean_m_s": -4.8564068748428524e-05,
  "peak_tilt_rad": 0.152417808639153,
  "peak_wheel_torque_nm": 8.201251029968262,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.049525652029464684,
  "final_integral_m_s": -0.049525652029464684,
  "elapsed_wall_s": 10.022253441042267
}
```
