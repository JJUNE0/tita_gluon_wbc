# tita_flash_sac_115632_883848_model_45000_kick+0.2_v03_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 43062a7c7858bfeb0cce0542eb1f4a18dfcde51a093f58d89c7806ec35643067

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_45000_kick+0.2_v03_s917",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_45000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 917,
    "estimator": "fk",
    "guarded": true,
    "kick": 0.2,
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
  "initial_physics_sha256": "ea4263088e8f522b8eb4c34f320c53f11803e6e22c7eb9d3a5e425277f8c6c69",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.05901580338097765,
  "max_drift_m": 0.10375524045272123,
  "radial_IAE_m_s": 3.7330164224747984,
  "signed_longitudinal_delta_m": 0.05898393629583447,
  "tail_speed_mean_m_s": -0.0001417260076504729,
  "tail_speed_rms_m_s": 0.007483256242520019,
  "tail_sensor_speed_mean_m_s": -0.0010733855840851989,
  "tail_fk_speed_mean_m_s": 4.949338764742032e-05,
  "peak_tilt_rad": 0.06354380129010351,
  "peak_wheel_torque_nm": 4.173892498016357,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.14883937376088247,
  "final_integral_m_s": 0.14883937376088247,
  "elapsed_wall_s": 13.214913537027314
}
```
