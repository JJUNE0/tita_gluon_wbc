# tita_flash_sac_193248_068255_model_85000_friction08_v03_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 520e4e186e62e77bd04fecac7cdf45838dad108ef710de3f9088dd03a7b3223b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_85000_friction08_v03_s916",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_85000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "friction": 0.8
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
  "checkpoint_sha256": "520e4e186e62e77bd04fecac7cdf45838dad108ef710de3f9088dd03a7b3223b",
  "onnx_sha256": "5d2438e3be90051d15448f31e014bdcdd44f963c2caabea6f5c8a62f0c9e2e0e",
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
  "initial_physics_sha256": "cbd5286036469307dc8a34b48bf8217f8f809607ca629fe085e47fed2ec29884",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.003946897840586364,
  "max_drift_m": 0.0410626484815666,
  "radial_IAE_m_s": 0.3567908938810196,
  "signed_longitudinal_delta_m": 0.00394679941484213,
  "tail_speed_mean_m_s": 5.47526061237428e-05,
  "tail_speed_rms_m_s": 0.0014718017918282705,
  "tail_sensor_speed_mean_m_s": 4.81111702100498e-05,
  "tail_fk_speed_mean_m_s": 5.4568068899441663e-05,
  "peak_tilt_rad": 0.05818463738718882,
  "peak_wheel_torque_nm": 0.5536198616027832,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.18209050974542373,
  "final_integral_m_s": 0.18209050974542373,
  "elapsed_wall_s": 10.173578493006062
}
```
