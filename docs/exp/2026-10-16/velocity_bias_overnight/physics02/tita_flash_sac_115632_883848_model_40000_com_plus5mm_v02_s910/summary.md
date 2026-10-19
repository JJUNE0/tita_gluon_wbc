# tita_flash_sac_115632_883848_model_40000_com_plus5mm_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a4b5c15c3add7114e65d55cabbe505c0fffcd993df1b9162587e073cca97a891

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_40000_com_plus5mm_v02_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_40000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "com": 0.005
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
  "initial_physics_sha256": "b7e617799832ffa230e5101505bb37e79d035e2c96e37c51fc3147d7c22e4893",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.0260796112011502,
  "max_drift_m": 0.0487879392868229,
  "radial_IAE_m_s": 1.5520293265324283,
  "signed_longitudinal_delta_m": 0.02607865139423366,
  "tail_speed_mean_m_s": 1.623508467847888e-05,
  "tail_speed_rms_m_s": 1.6285737936047667e-05,
  "tail_sensor_speed_mean_m_s": 1.5640126189599652e-05,
  "tail_fk_speed_mean_m_s": 1.776314175554418e-05,
  "peak_tilt_rad": 0.11754237225211162,
  "peak_wheel_torque_nm": 1.0720363855361938,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.27468748755295935,
  "final_integral_m_s": 0.2746574248133518,
  "elapsed_wall_s": 11.833634203998372
}
```
