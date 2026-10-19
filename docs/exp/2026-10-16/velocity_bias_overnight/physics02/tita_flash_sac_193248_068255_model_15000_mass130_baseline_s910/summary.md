# tita_flash_sac_193248_068255_model_15000_mass130_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 04a29ff5621d73fe8056a8ebcd44f66a2477b5d8bc0514955a419f6b336e2081

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_15000_mass130_baseline_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_15000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "mass": 1.3
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "04a29ff5621d73fe8056a8ebcd44f66a2477b5d8bc0514955a419f6b336e2081",
  "onnx_sha256": "2c397ad5d7dbe000ce3559aa35152f7b9a9662e19a7069baff210d46a88a6cb4",
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
  "initial_physics_sha256": "2294315ce0312aaeb6454b527ca167e1cc8771f409ccda3c5ba4643b2ca3a23b",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 3.9863723701752276,
  "max_drift_m": 3.9863723701752276,
  "radial_IAE_m_s": 119.9395501225356,
  "signed_longitudinal_delta_m": -3.93936106261831,
  "tail_speed_mean_m_s": -0.06663859474680159,
  "tail_speed_rms_m_s": 0.06996153740957835,
  "tail_sensor_speed_mean_m_s": -0.06574570671336005,
  "tail_fk_speed_mean_m_s": -0.06674355754838886,
  "peak_tilt_rad": 0.13479381216337516,
  "peak_wheel_torque_nm": 3.8699355125427246,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 12.237805181008298
}
```
