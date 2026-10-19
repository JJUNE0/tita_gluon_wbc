# tita_flash_sac_193248_068255_model_15000_mass130_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 04a29ff5621d73fe8056a8ebcd44f66a2477b5d8bc0514955a419f6b336e2081

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_15000_mass130_baseline_s916",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_15000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "mass": 1.3
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
  "initial_physics_sha256": "dfe7a33e1ad8464382e4ef23de73fd17b8b8739d907a38d91caab6b75ce73c71",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 3.9863727987713875,
  "max_drift_m": 3.9863727987713875,
  "radial_IAE_m_s": 119.93955859847705,
  "signed_longitudinal_delta_m": -3.939361747085536,
  "tail_speed_mean_m_s": -0.06663859826038532,
  "tail_speed_rms_m_s": 0.06996154230632066,
  "tail_sensor_speed_mean_m_s": -0.0657457310873663,
  "tail_fk_speed_mean_m_s": -0.06674356408397415,
  "peak_tilt_rad": 0.134793736303918,
  "peak_wheel_torque_nm": 3.8699305057525635,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 10.8769944839878
}
```
