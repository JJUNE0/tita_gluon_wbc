# p003_tita_flash_sac_115632_883848_model_45000

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 43062a7c7858bfeb0cce0542eb1f4a18dfcde51a093f58d89c7806ec35643067

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "p003_tita_flash_sac_115632_883848_model_45000",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_45000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "analytic",
    "physics": {
      "mass": 1.3
    },
    "kick": 0.0,
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0,
      "kp_fast": 5.0,
      "gain_velocity": 0.1,
      "gain_tau": 1.0,
      "gain_floor": 0.25
    }
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
  "initial_physics_sha256": "3a4ba1ca68189c8896b3491841cd28abf61e8aa5305f036f14ac64ec8a9f372d",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.020614367391906318,
  "max_drift_m": 0.0795973418994245,
  "radial_IAE_m_s": 1.3607717104844008,
  "signed_longitudinal_delta_m": 0.020609774179589972,
  "tail_speed_mean_m_s": -7.348283138227902e-05,
  "tail_speed_rms_m_s": 7.364254929105853e-05,
  "tail_sensor_speed_mean_m_s": -7.2892285496772e-05,
  "tail_fk_speed_mean_m_s": -7.091504924406956e-05,
  "peak_tilt_rad": 0.16672679549935943,
  "peak_wheel_torque_nm": 2.708388090133667,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.35064590626730324,
  "final_integral_m_s": -0.35061610912012836,
  "elapsed_wall_s": 9.40803482499905
}
```
