# tita_flash_sac_115632_883848_model_40000_friction08_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a4b5c15c3add7114e65d55cabbe505c0fffcd993df1b9162587e073cca97a891

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_40000_friction08_v02_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_40000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "friction": 0.8
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
  "initial_physics_sha256": "9466b55bf5cd6e8cd6d708cde14fd8284261c9384312072c3fcb4a6a53aab8f3",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.021549269210145102,
  "max_drift_m": 0.03893213289519651,
  "radial_IAE_m_s": 1.2778710991745341,
  "signed_longitudinal_delta_m": 0.021549010489614523,
  "tail_speed_mean_m_s": 1.570550343523881e-05,
  "tail_speed_rms_m_s": 1.576226817880773e-05,
  "tail_sensor_speed_mean_m_s": 1.7228633603675557e-05,
  "tail_fk_speed_mean_m_s": 1.9842522395692148e-05,
  "peak_tilt_rad": 0.11384062563168396,
  "peak_wheel_torque_nm": 0.899296760559082,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.2298350574825341,
  "final_integral_m_s": 0.22979811652230064,
  "elapsed_wall_s": 12.11240383196855
}
```
