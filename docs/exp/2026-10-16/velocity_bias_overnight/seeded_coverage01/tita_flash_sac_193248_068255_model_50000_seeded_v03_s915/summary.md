# tita_flash_sac_193248_068255_model_50000_seeded_v03_s915

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 948c108cb4740ede74b9c33fdca02f3a0bc4ae70aeb862e20f90c841243b1087

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_50000_seeded_v03_s915",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_50000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 915,
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
  "initial_physics_sha256": "ff4720828ac2047c5481fcc5a9ee44c1d2d0356bfa05c22c621ae57091f3623c",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.11860604062946117,
  "max_drift_m": 0.11860604062946117,
  "radial_IAE_m_s": 6.756508217796505,
  "signed_longitudinal_delta_m": 0.11860562919505004,
  "tail_speed_mean_m_s": 4.790657162853706e-05,
  "tail_speed_rms_m_s": 4.8625122509323835e-05,
  "tail_sensor_speed_mean_m_s": 4.781320208012392e-05,
  "tail_fk_speed_mean_m_s": 4.879454218680365e-05,
  "peak_tilt_rad": 0.05115233386986073,
  "peak_wheel_torque_nm": 0.5776048302650452,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.6983618447521862,
  "final_integral_m_s": 0.6983618447521862,
  "elapsed_wall_s": 4.675386691989843
}
```
