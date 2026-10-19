# p004_tita_flash_sac_115632_883848_model_45000

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 43062a7c7858bfeb0cce0542eb1f4a18dfcde51a093f58d89c7806ec35643067

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "p004_tita_flash_sac_115632_883848_model_45000",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_45000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "physics": {
      "mass": 1.3
    },
    "kick": 0.0,
    "law": {
      "kp": 0.0,
      "ki": 3.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0,
      "seed_gain": 4.0
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
  "final_drift_m": 0.10316013858420316,
  "max_drift_m": 0.12448154514925205,
  "radial_IAE_m_s": 6.177084539278255,
  "signed_longitudinal_delta_m": 0.10315725231597164,
  "tail_speed_mean_m_s": -6.0597369468313944e-05,
  "tail_speed_rms_m_s": 6.093178346853406e-05,
  "tail_sensor_speed_mean_m_s": -6.004289708875413e-05,
  "tail_fk_speed_mean_m_s": -5.802343724668754e-05,
  "peak_tilt_rad": 0.15225908377145814,
  "peak_wheel_torque_nm": 2.1642603874206543,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.3507439981491231,
  "final_integral_m_s": -0.3507439981491231,
  "elapsed_wall_s": 5.543967527977657
}
```
