# tita_flash_sac_193248_068255_model_30000_friction08_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 1e8eb8c4549e7335f4ef3d31ec9b7b45fd0cb148283a41b8c616f429cefb643f

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_30000_friction08_baseline_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_30000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "friction": 0.8
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
  },
  "checkpoint_sha256": "1e8eb8c4549e7335f4ef3d31ec9b7b45fd0cb148283a41b8c616f429cefb643f",
  "onnx_sha256": "ec18f72b80fd3755cb0dce2de3434e16c4375a38100a8a08c28560539614d4a8",
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
  "initial_physics_sha256": "abfa753d438462e9f791c714d594e6a5d8a725be528d5b24402b8ab1c0e90245",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 2.9506376819480726,
  "max_drift_m": 2.9506376819480726,
  "radial_IAE_m_s": 88.58897629040632,
  "signed_longitudinal_delta_m": 2.9502569278552913,
  "tail_speed_mean_m_s": 0.049056800212225186,
  "tail_speed_rms_m_s": 0.04905704081379874,
  "tail_sensor_speed_mean_m_s": 0.04895967183849212,
  "tail_fk_speed_mean_m_s": 0.04895864180285866,
  "peak_tilt_rad": 0.01865357154865399,
  "peak_wheel_torque_nm": 0.1588013768196106,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.836638622975443
}
```
