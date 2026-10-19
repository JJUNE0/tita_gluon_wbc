# tita_flash_sac_193248_068255_model_50000_kick+0.2_baseline_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 948c108cb4740ede74b9c33fdca02f3a0bc4ae70aeb862e20f90c841243b1087

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_50000_kick+0.2_baseline_s912",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_50000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 912,
    "estimator": "fk",
    "runtime": false,
    "kick": 0.2,
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
  "initial_physics_sha256": "3b4f0c72436a68a0dac951af1c44b9acc40dc2a85ec5169a0f8670d53f4176b6",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 7.341638745486721,
  "max_drift_m": 7.341638745486721,
  "radial_IAE_m_s": 217.27723483069556,
  "signed_longitudinal_delta_m": 7.340997617518098,
  "tail_speed_mean_m_s": 0.12669912563803162,
  "tail_speed_rms_m_s": 0.12670319223738233,
  "tail_sensor_speed_mean_m_s": 0.1264253405662252,
  "tail_fk_speed_mean_m_s": 0.12642360570979036,
  "peak_tilt_rad": 0.0797506897302156,
  "peak_wheel_torque_nm": 1.4924774169921875,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 10.04570702498313
}
```
