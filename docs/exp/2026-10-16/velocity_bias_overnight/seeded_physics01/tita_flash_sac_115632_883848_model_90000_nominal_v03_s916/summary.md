# tita_flash_sac_115632_883848_model_90000_nominal_v03_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 4930085834f72c133d65563169762514342959361a6d71630216f5f608b0531f

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_90000_nominal_v03_s916",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_90000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": true,
    "physics": {},
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
  "checkpoint_sha256": "4930085834f72c133d65563169762514342959361a6d71630216f5f608b0531f",
  "onnx_sha256": "1d6ffa5d91a15cf74e2abf755c367c1fb151f6e3c740618a6e1fb2fbf28f9379",
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
  "initial_physics_sha256": "2b0d5af7b92025700a304b816f0e78caaea4ef6a3548462404c42ff090edab32",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.044596307070400444,
  "max_drift_m": 0.05946644897901339,
  "radial_IAE_m_s": 2.5127559470527427,
  "signed_longitudinal_delta_m": 0.04459477589621101,
  "tail_speed_mean_m_s": 8.459518926762147e-05,
  "tail_speed_rms_m_s": 8.579690804941148e-05,
  "tail_sensor_speed_mean_m_s": 8.411057360179102e-05,
  "tail_fk_speed_mean_m_s": 8.529844120419308e-05,
  "peak_tilt_rad": 0.069167477133522,
  "peak_wheel_torque_nm": 0.41307151317596436,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.38911362134585703,
  "final_integral_m_s": 0.38911362134585703,
  "elapsed_wall_s": 10.837385780003387
}
```
