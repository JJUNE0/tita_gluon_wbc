# p009_tita_flash_sac_115632_883848_model_60000_kick+0.0

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "p009_tita_flash_sac_115632_883848_model_60000_kick+0.0",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_60000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 915,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "mass": 1.3
    },
    "kick": 0.0,
    "law": {
      "kp": 0.0,
      "ki": 4.0,
      "tau": 0.1,
      "ramp": 0.5,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 1.0,
      "seed_gain": 3.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
  },
  "checkpoint_sha256": "6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05",
  "onnx_sha256": "f44f07ed44970e3ff565eae67fd9229adf0be5c02215591c52a691ffcbb71b2a",
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
  "initial_physics_sha256": "c7221b1424dccd511978e6bd647df4fd09f235f0fbdb8175f1a17b1c88d15e6f",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.00274741010121445,
  "max_drift_m": 0.08391443024599661,
  "radial_IAE_m_s": 0.37756264368694825,
  "signed_longitudinal_delta_m": -0.0027327559074704546,
  "tail_speed_mean_m_s": 7.542625559841666e-05,
  "tail_speed_rms_m_s": 0.011730379535754886,
  "tail_sensor_speed_mean_m_s": -0.0007531006085763805,
  "tail_fk_speed_mean_m_s": -1.1664919866675063e-06,
  "peak_tilt_rad": 0.17546987906428702,
  "peak_wheel_torque_nm": 4.038240432739258,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.41769168878074836,
  "final_integral_m_s": -0.41769168878074836,
  "elapsed_wall_s": 10.03703507897444
}
```
