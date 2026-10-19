# tita_flash_sac_115632_883848_model_40000

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a4b5c15c3add7114e65d55cabbe505c0fffcd993df1b9162587e073cca97a891

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_40000",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_40000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 270,
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
  "initial_physics_sha256": "1c6ec06e13e84058a109d773d6ec016e360c8bc50213598ac915fa56f8006fbe",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 7.093039114810091,
  "max_drift_m": 7.093039114810091,
  "radial_IAE_m_s": 213.51549464821656,
  "signed_longitudinal_delta_m": 7.088959182536628,
  "tail_speed_mean_m_s": 0.1173046015113237,
  "tail_speed_rms_m_s": 0.11730510892955344,
  "tail_sensor_speed_mean_m_s": 0.11705094902259301,
  "tail_fk_speed_mean_m_s": 0.11705116852879136,
  "peak_tilt_rad": 0.11500566688406177,
  "peak_wheel_torque_nm": 0.22923946380615234,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 4.471173348953016
}
```
