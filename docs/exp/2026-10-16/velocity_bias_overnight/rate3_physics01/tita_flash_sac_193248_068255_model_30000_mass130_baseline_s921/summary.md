# tita_flash_sac_193248_068255_model_30000_mass130_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 1e8eb8c4549e7335f4ef3d31ec9b7b45fd0cb148283a41b8c616f429cefb643f

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_30000_mass130_baseline_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_30000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "mass": 1.3
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
  "initial_physics_sha256": "ee1cfa4be13f4b71e6c8afa325079e1125c6e2a2b49bbdd18096264b49ea7d2e",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 9.3022731798408,
  "max_drift_m": 9.3022731798408,
  "radial_IAE_m_s": 279.66275219000283,
  "signed_longitudinal_delta_m": -9.111079813796419,
  "tail_speed_mean_m_s": -0.15617803663092208,
  "tail_speed_rms_m_s": 0.15617804806895988,
  "tail_sensor_speed_mean_m_s": -0.15584214492080561,
  "tail_fk_speed_mean_m_s": -0.1558312512389034,
  "peak_tilt_rad": 0.011840592150775526,
  "peak_wheel_torque_nm": 0.3468656539916992,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 8.892788527009543
}
```
