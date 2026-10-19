# tita_flash_sac_115632_883848_model_60000_mass1.15_v01

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_60000_mass1.15_v01",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_60000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 272,
    "physics": {
      "mass": 1.15
    },
    "kick": 0.0,
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.05,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
    },
    "estimator": "fk"
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
  "initial_physics_sha256": "0035c473643c9ac44fca17820f236d495acfe9480e24dd190457dfb5f45dac66",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.021172755940651582,
  "max_drift_m": 0.03776668894646887,
  "radial_IAE_m_s": 1.2748218258416475,
  "signed_longitudinal_delta_m": -0.021172622774585252,
  "tail_speed_mean_m_s": -8.000038589495185e-06,
  "tail_speed_rms_m_s": 1.0421597852739805e-05,
  "tail_sensor_speed_mean_m_s": -7.630729219312318e-06,
  "tail_fk_speed_mean_m_s": -6.738041995111848e-06,
  "peak_tilt_rad": 0.11700755582499123,
  "peak_wheel_torque_nm": 0.9145946502685547,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.22253878286038786,
  "final_integral_m_s": -0.2225120091544899,
  "elapsed_wall_s": 5.4447692219982855
}
```
