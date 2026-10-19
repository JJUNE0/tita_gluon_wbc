# tita_flash_sac_115632_883848_model_45000_kick-0.2_v03_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 43062a7c7858bfeb0cce0542eb1f4a18dfcde51a093f58d89c7806ec35643067

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_45000_kick-0.2_v03_s917",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_45000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 917,
    "estimator": "fk",
    "guarded": true,
    "kick": -0.2,
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
  "initial_physics_sha256": "6ff96664336f59668c00b70abad85e3fbb9dd5e7f4e96d753c8af88984596612",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.05667634511719646,
  "max_drift_m": 0.06297090216712799,
  "radial_IAE_m_s": 3.4473813309022994,
  "signed_longitudinal_delta_m": 0.0566601797397372,
  "tail_speed_mean_m_s": -3.586256056294663e-05,
  "tail_speed_rms_m_s": 0.007463737357007687,
  "tail_sensor_speed_mean_m_s": 0.0015147084238987644,
  "tail_fk_speed_mean_m_s": 7.056912099659291e-05,
  "peak_tilt_rad": 0.0804254354321936,
  "peak_wheel_torque_nm": 3.3127377033233643,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.15412729300776115,
  "final_integral_m_s": 0.15412729300776115,
  "elapsed_wall_s": 12.140304053958971
}
```
