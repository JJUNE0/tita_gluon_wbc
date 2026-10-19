# tita_flash_sac_115632_883848_model_40000_nominal_v03_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a4b5c15c3add7114e65d55cabbe505c0fffcd993df1b9162587e073cca97a891

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_40000_nominal_v03_s916",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_40000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": true,
    "physics": {},
    "law": {
      "kp": 0.0,
      "ki": 4.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0,
      "seed_gain": 3.0
    },
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
  },
  "checkpoint_sha256": "a4b5c15c3add7114e65d55cabbe505c0fffcd993df1b9162587e073cca97a891",
  "onnx_sha256": "4722a7e5dc4a1d465689d98943ba5c9a40a7d45a99344f923f067d1cfa90fcb6",
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
  "initial_physics_sha256": "a22ad6714028879f84d294c68d90119e38967604c7da8ea5feb20ae0d9cb2c26",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.0048024710617871405,
  "max_drift_m": 0.03976565140149912,
  "radial_IAE_m_s": 0.4043461526613203,
  "signed_longitudinal_delta_m": -0.004798659791931722,
  "tail_speed_mean_m_s": 4.255475909187037e-05,
  "tail_speed_rms_m_s": 4.258551605744001e-05,
  "tail_sensor_speed_mean_m_s": 4.191909150120993e-05,
  "tail_fk_speed_mean_m_s": 4.431121838737757e-05,
  "peak_tilt_rad": 0.11353211166831301,
  "peak_wheel_torque_nm": 0.8932968378067017,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.23332767962422482,
  "final_integral_m_s": 0.23332767962422482,
  "elapsed_wall_s": 11.756354269047733
}
```
