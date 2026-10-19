# tita_flash_sac_115632_883848_model_45000_com_plus5mm_v03_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 43062a7c7858bfeb0cce0542eb1f4a18dfcde51a093f58d89c7806ec35643067

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_45000_com_plus5mm_v03_s916",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_45000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "com": 0.005
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
  "initial_physics_sha256": "7b468b946dbebe3bcf1fd6cdabb26d5cc33dceabaacec4c28e2c27966abf98bc",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.002507266341542649,
  "max_drift_m": 0.015087254704677307,
  "radial_IAE_m_s": 0.24387202530806723,
  "signed_longitudinal_delta_m": 0.001963105527565231,
  "tail_speed_mean_m_s": -9.350137641168459e-05,
  "tail_speed_rms_m_s": 0.0075335594762436855,
  "tail_sensor_speed_mean_m_s": 0.0008382929022936544,
  "tail_fk_speed_mean_m_s": 0.00014223440697643406,
  "peak_tilt_rad": 0.039926112620452425,
  "peak_wheel_torque_nm": 2.5416343212127686,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.1662730395429023,
  "final_integral_m_s": 0.1662730395429023,
  "elapsed_wall_s": 12.360396361036692
}
```
