# tita_flash_sac_193248_068255_model_15000_mass130_v03_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 04a29ff5621d73fe8056a8ebcd44f66a2477b5d8bc0514955a419f6b336e2081

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_15000_mass130_v03_s916",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_15000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
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
      "slew": 2.0,
      "seed_gain": 3.0
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
  "final_drift_m": 0.033638588849368135,
  "max_drift_m": 0.04251762786337217,
  "radial_IAE_m_s": 2.196398676881047,
  "signed_longitudinal_delta_m": -0.033601083245834405,
  "tail_speed_mean_m_s": 4.972459271870808e-05,
  "tail_speed_rms_m_s": 0.019035178964684037,
  "tail_sensor_speed_mean_m_s": 0.0016063689990093257,
  "tail_fk_speed_mean_m_s": 7.086387649693305e-05,
  "peak_tilt_rad": 0.17337678325058326,
  "peak_wheel_torque_nm": 4.477106094360352,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.33168428929297733,
  "final_integral_m_s": -0.33168428929297733,
  "elapsed_wall_s": 10.666075979999732
}
```
