# tita_flash_sac_115632_883848_model_40000_tau0.1_entry12

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a4b5c15c3add7114e65d55cabbe505c0fffcd993df1b9162587e073cca97a891

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_40000_tau0.1_entry12",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_40000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 271,
    "estimator": "fk",
    "runtime": true,
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
  "initial_physics_sha256": "c0bbcda7fba701c507620ba5ff12e1cb329f2d2b0cdf7a9d71ac7e299972a818",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.022253685574189563,
  "max_drift_m": 0.03968423352978084,
  "radial_IAE_m_s": 1.3171799222262868,
  "signed_longitudinal_delta_m": 0.022252096106536695,
  "tail_speed_mean_m_s": 1.651162272522088e-05,
  "tail_speed_rms_m_s": 1.657332694806443e-05,
  "tail_sensor_speed_mean_m_s": 1.5991897449915997e-05,
  "tail_fk_speed_mean_m_s": 1.834764624958152e-05,
  "peak_tilt_rad": 0.11350760801795179,
  "peak_wheel_torque_nm": 0.9394537210464478,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.2341337333559837,
  "final_integral_m_s": 0.2340920942823206,
  "elapsed_wall_s": 5.995188609987963
}
```
