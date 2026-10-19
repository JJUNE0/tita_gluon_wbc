# tita_flash_sac_115632_883848_model_40000_nominal_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a4b5c15c3add7114e65d55cabbe505c0fffcd993df1b9162587e073cca97a891

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_40000_nominal_v02_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_40000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {},
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
  "initial_physics_sha256": "683fa4ba7df54ced3d1db3178267e151195a0e2fc7c50832bd72abffc8b2686d",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.022297149649062247,
  "max_drift_m": 0.03974268699868451,
  "radial_IAE_m_s": 1.3196126765093514,
  "signed_longitudinal_delta_m": 0.022295557060496993,
  "tail_speed_mean_m_s": 1.680874311603826e-05,
  "tail_speed_rms_m_s": 1.688127248092603e-05,
  "tail_sensor_speed_mean_m_s": 1.6322900821198106e-05,
  "tail_fk_speed_mean_m_s": 1.8656018466882732e-05,
  "peak_tilt_rad": 0.113481326356206,
  "peak_wheel_torque_nm": 0.9427878856658936,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.23453212971249002,
  "final_integral_m_s": 0.23449048048702156,
  "elapsed_wall_s": 11.654953096993268
}
```
