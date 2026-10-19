# tita_flash_sac_115632_883848_model_45000_seeded_v03_s915

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 43062a7c7858bfeb0cce0542eb1f4a18dfcde51a093f58d89c7806ec35643067

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_45000_seeded_v03_s915",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_45000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 915,
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
  "checkpoint_sha256": "43062a7c7858bfeb0cce0542eb1f4a18dfcde51a093f58d89c7806ec35643067",
  "onnx_sha256": "7b25c8c9afe56cdbfe483aa15167008f11b20e96722bf811b19fa3d80bf0e8e5",
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
  "initial_physics_sha256": "761f8fcecb26311455fbe17d54cd57c8d228feca13c75964b34c31eb8c1d80f8",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.0029527138034434715,
  "max_drift_m": 0.012781381830797325,
  "radial_IAE_m_s": 0.24835772437629317,
  "signed_longitudinal_delta_m": 0.002816744829310675,
  "tail_speed_mean_m_s": -4.9148971837503285e-05,
  "tail_speed_rms_m_s": 0.007442616109123437,
  "tail_sensor_speed_mean_m_s": -0.00037468009084316547,
  "tail_fk_speed_mean_m_s": -0.00010086869044245086,
  "peak_tilt_rad": 0.03785622179572323,
  "peak_wheel_torque_nm": 2.598012685775757,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.1526573685127774,
  "final_integral_m_s": 0.1526573685127774,
  "elapsed_wall_s": 4.611752626020461
}
```
