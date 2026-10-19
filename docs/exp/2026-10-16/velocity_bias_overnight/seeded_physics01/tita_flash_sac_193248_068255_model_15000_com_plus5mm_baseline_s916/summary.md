# tita_flash_sac_193248_068255_model_15000_com_plus5mm_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 04a29ff5621d73fe8056a8ebcd44f66a2477b5d8bc0514955a419f6b336e2081

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_15000_com_plus5mm_baseline_s916",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_15000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "com": 0.005
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
  },
  "checkpoint_sha256": "04a29ff5621d73fe8056a8ebcd44f66a2477b5d8bc0514955a419f6b336e2081",
  "onnx_sha256": "2c397ad5d7dbe000ce3559aa35152f7b9a9662e19a7069baff210d46a88a6cb4",
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
  "initial_physics_sha256": "3a44facb4de9bc021aae42f80defa491e2eee5124fb0fbe69faa318a2b910127",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 2.6312211456320855,
  "max_drift_m": 2.6312211456320855,
  "radial_IAE_m_s": 79.00407082165478,
  "signed_longitudinal_delta_m": -2.6270725648415776,
  "tail_speed_mean_m_s": -0.04381814688779892,
  "tail_speed_rms_m_s": 0.04381815137959491,
  "tail_sensor_speed_mean_m_s": -0.04373375698709876,
  "tail_fk_speed_mean_m_s": -0.04372958732808548,
  "peak_tilt_rad": 0.04798214876814155,
  "peak_wheel_torque_nm": 0.06886433064937592,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 10.708560857980046
}
```
