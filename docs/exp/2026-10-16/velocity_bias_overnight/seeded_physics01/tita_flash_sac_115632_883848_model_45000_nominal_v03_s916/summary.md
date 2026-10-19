# tita_flash_sac_115632_883848_model_45000_nominal_v03_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 43062a7c7858bfeb0cce0542eb1f4a18dfcde51a093f58d89c7806ec35643067

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_45000_nominal_v03_s916",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_45000",
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
  "initial_physics_sha256": "934a92bf0c25df7b95f8ca15e8735ab402f924d403b79c2ad82feaf963faec46",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.0031582136476579407,
  "max_drift_m": 0.012665202039034004,
  "radial_IAE_m_s": 0.2555647597299299,
  "signed_longitudinal_delta_m": 0.0030322407564379894,
  "tail_speed_mean_m_s": -5.124899680001299e-05,
  "tail_speed_rms_m_s": 0.007477100488705241,
  "tail_sensor_speed_mean_m_s": -0.00043530585472358724,
  "tail_fk_speed_mean_m_s": -0.00010225913200187327,
  "peak_tilt_rad": 0.0380093686267442,
  "peak_wheel_torque_nm": 2.598874568939209,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.15234982291155308,
  "final_integral_m_s": 0.15234982291155308,
  "elapsed_wall_s": 11.080447062035091
}
```
