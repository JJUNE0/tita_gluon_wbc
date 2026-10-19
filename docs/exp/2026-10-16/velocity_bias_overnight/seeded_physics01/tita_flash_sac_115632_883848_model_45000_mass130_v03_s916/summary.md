# tita_flash_sac_115632_883848_model_45000_mass130_v03_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 43062a7c7858bfeb0cce0542eb1f4a18dfcde51a093f58d89c7806ec35643067

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_45000_mass130_v03_s916",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_45000",
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
  "initial_physics_sha256": "faa3eff743868275db059e4ae532b312ac8d884881a7f77f66b391b3f9549b8e",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.03683538456840147,
  "max_drift_m": 0.06769518550645055,
  "radial_IAE_m_s": 2.2787992812516826,
  "signed_longitudinal_delta_m": 0.03683205695076858,
  "tail_speed_mean_m_s": -4.6155944522148964e-05,
  "tail_speed_rms_m_s": 4.640820224704051e-05,
  "tail_sensor_speed_mean_m_s": -4.5620264385750563e-05,
  "tail_fk_speed_mean_m_s": -4.361136248255419e-05,
  "peak_tilt_rad": 0.14556756179516395,
  "peak_wheel_torque_nm": 3.1067404747009277,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.3507247786219032,
  "final_integral_m_s": -0.3507247786219032,
  "elapsed_wall_s": 12.875147856015246
}
```
