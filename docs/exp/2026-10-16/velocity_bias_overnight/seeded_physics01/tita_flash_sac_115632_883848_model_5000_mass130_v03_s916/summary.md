# tita_flash_sac_115632_883848_model_5000_mass130_v03_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: cc685c5efb437641f8ad47131a1b737aa37ee01ecbc81e3d5e5a21ebc1ddd90d

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_5000_mass130_v03_s916",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_5000",
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
  "checkpoint_sha256": "cc685c5efb437641f8ad47131a1b737aa37ee01ecbc81e3d5e5a21ebc1ddd90d",
  "onnx_sha256": "4d80b373930fd59198e3fc588870f929175201ad8b748405f7e94231464a4d30",
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
  "initial_physics_sha256": "334abd69d138a22037685971592964b58e1cffbf37a9886ac9e1b11172c6a8e8",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.017931372069394824,
  "max_drift_m": 0.020713267041319594,
  "radial_IAE_m_s": 0.5333346484185386,
  "signed_longitudinal_delta_m": -0.016691959245292858,
  "tail_speed_mean_m_s": -0.0004135458402638798,
  "tail_speed_rms_m_s": 0.01722168786903716,
  "tail_sensor_speed_mean_m_s": -6.368387161070899e-05,
  "tail_fk_speed_mean_m_s": 6.747588959314168e-06,
  "peak_tilt_rad": 0.1880608653898519,
  "peak_wheel_torque_nm": 3.653581142425537,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.14649511504491775,
  "final_integral_m_s": -0.14649511504491775,
  "elapsed_wall_s": 11.99140526400879
}
```
