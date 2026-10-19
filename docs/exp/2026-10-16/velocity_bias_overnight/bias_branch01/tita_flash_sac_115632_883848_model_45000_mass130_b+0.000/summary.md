# tita_flash_sac_115632_883848_model_45000_mass130_b+0.000

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 43062a7c7858bfeb0cce0542eb1f4a18dfcde51a093f58d89c7806ec35643067

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_45000_mass130_b+0.000",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_45000",
    "duration": 120.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "physics": {
      "mass": 1.3
    },
    "law": {
      "mode": "constant",
      "bias": 0.0,
      "limit": 2.0,
      "slew": 2.0,
      "ramp": 0.25
    }
  },
  "checkpoint_sha256": "43062a7c7858bfeb0cce0542eb1f4a18dfcde51a093f58d89c7806ec35643067",
  "onnx_sha256": "7b25c8c9afe56cdbfe483aa15167008f11b20e96722bf811b19fa3d80bf0e8e5",
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
  "duration_s": 120.0,
  "final_drift_m": 16.629996647661546,
  "max_drift_m": 18.794370308090105,
  "radial_IAE_m_s": 1357.4381522221538,
  "signed_longitudinal_delta_m": -13.992695723698056,
  "tail_speed_mean_m_s": -0.1980083048208774,
  "tail_speed_rms_m_s": 0.19823980408207745,
  "tail_sensor_speed_mean_m_s": -0.19815525644745063,
  "tail_fk_speed_mean_m_s": -0.197699788222828,
  "peak_tilt_rad": 0.03736604388779874,
  "peak_wheel_torque_nm": 1.1814191341400146,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 22.895427834999282
}
```
