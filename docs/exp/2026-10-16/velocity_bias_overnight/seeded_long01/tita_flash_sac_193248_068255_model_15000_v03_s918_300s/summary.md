# tita_flash_sac_193248_068255_model_15000_v03_s918_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 04a29ff5621d73fe8056a8ebcd44f66a2477b5d8bc0514955a419f6b336e2081

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_15000_v03_s918_300s",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_15000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 918,
    "estimator": "fk",
    "guarded": true,
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
  "initial_physics_sha256": "c80e9569675d5c84dd0f32360724a83de26ec076f251ebb8f145e54acd2934d5",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.004107614102652373,
  "max_drift_m": 0.02385157954249381,
  "radial_IAE_m_s": 0.6756833525313846,
  "signed_longitudinal_delta_m": -0.004101022969081143,
  "tail_speed_mean_m_s": -1.2337767822023378e-05,
  "tail_speed_rms_m_s": 1.2342416341659165e-05,
  "tail_sensor_speed_mean_m_s": -1.1830934390834451e-05,
  "tail_fk_speed_mean_m_s": -9.365896270673507e-06,
  "peak_tilt_rad": 0.0953682818423005,
  "peak_wheel_torque_nm": 0.48033589124679565,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.19211135512994854,
  "final_integral_m_s": -0.19211135512994854,
  "elapsed_wall_s": 44.0943718549679
}
```
