# tita_flash_sac_115632_883848_model_40000_tau0.2_entry12

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a4b5c15c3add7114e65d55cabbe505c0fffcd993df1b9162587e073cca97a891

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_40000_tau0.2_entry12",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_40000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 271,
    "estimator": "fk",
    "runtime": true,
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.2,
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
  "final_drift_m": 0.022255403227070383,
  "max_drift_m": 0.04455684445812992,
  "radial_IAE_m_s": 1.3204668251925824,
  "signed_longitudinal_delta_m": 0.022254000210673468,
  "tail_speed_mean_m_s": 1.6551108732892405e-05,
  "tail_speed_rms_m_s": 1.661615858548815e-05,
  "tail_sensor_speed_mean_m_s": 1.6033367232020896e-05,
  "tail_fk_speed_mean_m_s": 1.8388153596227345e-05,
  "peak_tilt_rad": 0.11351348113401594,
  "peak_wheel_torque_nm": 0.7325554490089417,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.23416648495547893,
  "final_integral_m_s": 0.2341249106286781,
  "elapsed_wall_s": 5.904817622969858
}
```
