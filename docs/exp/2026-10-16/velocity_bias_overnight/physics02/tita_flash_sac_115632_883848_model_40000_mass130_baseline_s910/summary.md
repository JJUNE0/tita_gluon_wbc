# tita_flash_sac_115632_883848_model_40000_mass130_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a4b5c15c3add7114e65d55cabbe505c0fffcd993df1b9162587e073cca97a891

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_40000_mass130_baseline_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_40000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "mass": 1.3
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "a4b5c15c3add7114e65d55cabbe505c0fffcd993df1b9162587e073cca97a891",
  "onnx_sha256": "4722a7e5dc4a1d465689d98943ba5c9a40a7d45a99344f923f067d1cfa90fcb6",
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
  "initial_physics_sha256": "6fbd0dfbca224cf5c93ade53b233415a2a7df074ae5496163b425c9c1391d665",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 10.476739771282762,
  "max_drift_m": 10.476739771282762,
  "radial_IAE_m_s": 319.0198895000834,
  "signed_longitudinal_delta_m": -10.428970220879416,
  "tail_speed_mean_m_s": -0.17074735326824375,
  "tail_speed_rms_m_s": 0.17076278808261713,
  "tail_sensor_speed_mean_m_s": -0.1705161452389732,
  "tail_fk_speed_mean_m_s": -0.17052656518995918,
  "peak_tilt_rad": 0.07907890852214705,
  "peak_wheel_torque_nm": 0.24936270713806152,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.384383303986397
}
```
