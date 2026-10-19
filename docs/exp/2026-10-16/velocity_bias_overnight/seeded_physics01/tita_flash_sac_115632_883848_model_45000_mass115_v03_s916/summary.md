# tita_flash_sac_115632_883848_model_45000_mass115_v03_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 43062a7c7858bfeb0cce0542eb1f4a18dfcde51a093f58d89c7806ec35643067

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_45000_mass115_v03_s916",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_45000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "mass": 1.15
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
  "initial_physics_sha256": "d755a0c3cc817a9c0dd97297a4223282a2faa723ebaf7660ca8ea10661cd1af0",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.008174451835533933,
  "max_drift_m": 0.02466539440001881,
  "radial_IAE_m_s": 0.3643430657031477,
  "signed_longitudinal_delta_m": -0.00817393235346398,
  "tail_speed_mean_m_s": -7.992577777935831e-05,
  "tail_speed_rms_m_s": 0.0040255619676756995,
  "tail_sensor_speed_mean_m_s": -0.0004327031885465424,
  "tail_fk_speed_mean_m_s": -0.00010606003112665088,
  "peak_tilt_rad": 0.06786309124395928,
  "peak_wheel_torque_nm": 2.152413845062256,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.20947211203355326,
  "final_integral_m_s": -0.20947211203355326,
  "elapsed_wall_s": 14.2763856559759
}
```
