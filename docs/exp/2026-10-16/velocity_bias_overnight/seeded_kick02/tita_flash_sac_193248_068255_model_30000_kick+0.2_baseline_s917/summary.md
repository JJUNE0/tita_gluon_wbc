# tita_flash_sac_193248_068255_model_30000_kick+0.2_baseline_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 1e8eb8c4549e7335f4ef3d31ec9b7b45fd0cb148283a41b8c616f429cefb643f

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_30000_kick+0.2_baseline_s917",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_30000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 917,
    "estimator": "fk",
    "guarded": false,
    "kick": 0.2,
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
  "initial_physics_sha256": "52a95bae47cc5cf56b85602b94f748ae63b757087f5d33fced185b9ab6fbdc64",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 3.060575934216687,
  "max_drift_m": 3.060575934216687,
  "radial_IAE_m_s": 95.93288666367005,
  "signed_longitudinal_delta_m": 3.060185353400532,
  "tail_speed_mean_m_s": 0.04846143447260961,
  "tail_speed_rms_m_s": 0.0484616229201286,
  "tail_sensor_speed_mean_m_s": 0.0483561703179861,
  "tail_fk_speed_mean_m_s": 0.04835491060403152,
  "peak_tilt_rad": 0.05511424752512628,
  "peak_wheel_torque_nm": 1.238924264907837,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.176521564018913
}
```
