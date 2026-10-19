# tita_flash_sac_115632_883848_model_45000_kick+0.2_v04_s922

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 43062a7c7858bfeb0cce0542eb1f4a18dfcde51a093f58d89c7806ec35643067

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_45000_kick+0.2_v04_s922",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_45000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 922,
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
      "slew": 3.0,
      "seed_gain": 3.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
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
  "initial_physics_sha256": "f4daae14e49c8333b3cb4218158fc4bd4b580e115b1671d8bba6608948dd522d",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.004202698933695035,
  "max_drift_m": 0.08119933304452882,
  "radial_IAE_m_s": 0.46982409353672927,
  "signed_longitudinal_delta_m": 0.002969799007971791,
  "tail_speed_mean_m_s": -0.00013597150036132115,
  "tail_speed_rms_m_s": 0.007480142311099775,
  "tail_sensor_speed_mean_m_s": -0.0005104287418808655,
  "tail_fk_speed_mean_m_s": 8.91376486007661e-05,
  "peak_tilt_rad": 0.06216627059229718,
  "peak_wheel_torque_nm": 4.982628345489502,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.149268659285002,
  "final_integral_m_s": 0.149268659285002,
  "elapsed_wall_s": 9.754007727024145
}
```
