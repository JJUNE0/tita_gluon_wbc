# tita_flash_sac_115632_883848_model_40000_kick-0.2_v03_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a4b5c15c3add7114e65d55cabbe505c0fffcd993df1b9162587e073cca97a891

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_40000_kick-0.2_v03_s917",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_40000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 917,
    "estimator": "fk",
    "guarded": true,
    "kick": -0.2,
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
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
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
  "initial_physics_sha256": "9cf4c45ca5dadf3f1fe9a3041a959c19b0e92223264c87a706c8beacd9c01588",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.006196885961257916,
  "max_drift_m": 0.0406189297954218,
  "radial_IAE_m_s": 0.47921188344839405,
  "signed_longitudinal_delta_m": -0.006177123598429405,
  "tail_speed_mean_m_s": 4.2345440834601335e-05,
  "tail_speed_rms_m_s": 4.236067808935262e-05,
  "tail_sensor_speed_mean_m_s": 4.1694602620397855e-05,
  "tail_fk_speed_mean_m_s": 4.409786396615765e-05,
  "peak_tilt_rad": 0.11294439948613477,
  "peak_wheel_torque_nm": 1.7334305047988892,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.2331897117130841,
  "final_integral_m_s": 0.2331897117130841,
  "elapsed_wall_s": 13.26301048201276
}
```
