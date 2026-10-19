# tita_flash_sac_193248_068255_model_50000_v03_s918_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 948c108cb4740ede74b9c33fdca02f3a0bc4ae70aeb862e20f90c841243b1087

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_50000_v03_s918_300s",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_50000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 918,
    "estimator": "fk",
    "guarded": true,
    "law": {
      "kp": 0.0,
      "ki": 4.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0,
      "seed_gain": 3.0
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
  "initial_physics_sha256": "405f8845fae5e514bf7eb899589d0323d61c9f68adf6897cc6bdb9f05a2ec1a5",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.11729840685601298,
  "max_drift_m": 0.1209492842620311,
  "radial_IAE_m_s": 35.31274976546206,
  "signed_longitudinal_delta_m": 0.11729706721705849,
  "tail_speed_mean_m_s": 8.424302887022203e-06,
  "tail_speed_rms_m_s": 1.1995222126105811e-05,
  "tail_sensor_speed_mean_m_s": 7.927651700094559e-06,
  "tail_fk_speed_mean_m_s": 8.710437188777816e-06,
  "peak_tilt_rad": 0.05068324766809584,
  "peak_wheel_torque_nm": 0.5550882816314697,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.6867762776871497,
  "final_integral_m_s": 0.6867762776871497,
  "elapsed_wall_s": 49.87071270594606
}
```
