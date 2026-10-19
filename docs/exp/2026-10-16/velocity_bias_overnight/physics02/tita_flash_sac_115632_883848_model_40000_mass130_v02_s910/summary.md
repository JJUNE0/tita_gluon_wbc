# tita_flash_sac_115632_883848_model_40000_mass130_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a4b5c15c3add7114e65d55cabbe505c0fffcd993df1b9162587e073cca97a891

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_40000_mass130_v02_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_40000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "mass": 1.3
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
  "final_drift_m": 0.025997403411214273,
  "max_drift_m": 0.06448455384264186,
  "radial_IAE_m_s": 1.5561267814681603,
  "signed_longitudinal_delta_m": -0.025988310196426515,
  "tail_speed_mean_m_s": -1.4856810369941754e-05,
  "tail_speed_rms_m_s": 1.4880571093664714e-05,
  "tail_sensor_speed_mean_m_s": -1.5186380680992048e-05,
  "tail_fk_speed_mean_m_s": -1.6384161934355693e-05,
  "peak_tilt_rad": 0.20251288843834048,
  "peak_wheel_torque_nm": 1.722784399986267,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.2791286554051709,
  "final_integral_m_s": -0.27909833654895855,
  "elapsed_wall_s": 12.034464317024685
}
```
