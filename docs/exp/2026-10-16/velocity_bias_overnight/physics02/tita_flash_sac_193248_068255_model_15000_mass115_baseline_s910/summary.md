# tita_flash_sac_193248_068255_model_15000_mass115_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 04a29ff5621d73fe8056a8ebcd44f66a2477b5d8bc0514955a419f6b336e2081

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_15000_mass115_baseline_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_15000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "mass": 1.15
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
  "initial_physics_sha256": "e14c90838f319d7dd3057ff2ddccccb5704f8fec9a457442d5b515a6a7abadf9",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 4.802495071493895,
  "max_drift_m": 4.802495071493895,
  "radial_IAE_m_s": 143.42276791051415,
  "signed_longitudinal_delta_m": -4.797820959617267,
  "tail_speed_mean_m_s": -0.08042047801818551,
  "tail_speed_rms_m_s": 0.0807672406879412,
  "tail_sensor_speed_mean_m_s": -0.08086437142798418,
  "tail_fk_speed_mean_m_s": -0.08034342561159412,
  "peak_tilt_rad": 0.10235549971245184,
  "peak_wheel_torque_nm": 2.2670743465423584,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 12.024266296008136
}
```
