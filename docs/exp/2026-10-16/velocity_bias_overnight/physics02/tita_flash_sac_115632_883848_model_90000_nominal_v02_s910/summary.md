# tita_flash_sac_115632_883848_model_90000_nominal_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 4930085834f72c133d65563169762514342959361a6d71630216f5f608b0531f

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_90000_nominal_v02_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_90000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {},
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
    }
  },
  "checkpoint_sha256": "4930085834f72c133d65563169762514342959361a6d71630216f5f608b0531f",
  "onnx_sha256": "1d6ffa5d91a15cf74e2abf755c367c1fb151f6e3c740618a6e1fb2fbf28f9379",
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
  "initial_physics_sha256": "e71e604bf0e1061f3f76c5ca438ebedcba3a488858f7be286770f638e8be9d27",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.03826307344701975,
  "max_drift_m": 0.04787217777119549,
  "radial_IAE_m_s": 2.2239373719997415,
  "signed_longitudinal_delta_m": 0.038261978475696165,
  "tail_speed_mean_m_s": 3.565790520217503e-05,
  "tail_speed_rms_m_s": 3.631534164518711e-05,
  "tail_sensor_speed_mean_m_s": 3.529732468802217e-05,
  "tail_fk_speed_mean_m_s": 3.646484298725606e-05,
  "peak_tilt_rad": 0.0689796510214642,
  "peak_wheel_torque_nm": 0.4861220419406891,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.390594619525833,
  "final_integral_m_s": 0.39050300393416687,
  "elapsed_wall_s": 14.602613936993293
}
```
