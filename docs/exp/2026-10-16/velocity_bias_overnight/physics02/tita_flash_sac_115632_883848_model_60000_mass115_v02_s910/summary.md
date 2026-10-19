# tita_flash_sac_115632_883848_model_60000_mass115_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_60000_mass115_v02_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_60000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "mass": 1.15
    },
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
  "checkpoint_sha256": "6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05",
  "onnx_sha256": "f44f07ed44970e3ff565eae67fd9229adf0be5c02215591c52a691ffcbb71b2a",
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
  "initial_physics_sha256": "708b85f64ac481614c03670a578bec7f0d5b44bb459afcf70b2a1a339c249e4a",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.021415225901998777,
  "max_drift_m": 0.03501647538720446,
  "radial_IAE_m_s": 1.279686832555047,
  "signed_longitudinal_delta_m": -0.021415225559999772,
  "tail_speed_mean_m_s": -1.3772120797428634e-05,
  "tail_speed_rms_m_s": 1.4063638393760465e-05,
  "tail_sensor_speed_mean_m_s": -1.334284409376636e-05,
  "tail_fk_speed_mean_m_s": -1.2507220727029703e-05,
  "peak_tilt_rad": 0.11309210100799394,
  "peak_wheel_torque_nm": 0.6355785131454468,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.2236802880345737,
  "final_integral_m_s": -0.22365492193636788,
  "elapsed_wall_s": 15.613470955984667
}
```
