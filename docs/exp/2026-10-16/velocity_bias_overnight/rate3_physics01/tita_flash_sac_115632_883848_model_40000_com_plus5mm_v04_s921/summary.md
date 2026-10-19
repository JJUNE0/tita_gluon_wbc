# tita_flash_sac_115632_883848_model_40000_com_plus5mm_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a4b5c15c3add7114e65d55cabbe505c0fffcd993df1b9162587e073cca97a891

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_40000_com_plus5mm_v04_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_40000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "com": 0.005
    },
    "law": {
      "kp": 0.0,
      "ki": 4.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 3.0,
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
  "initial_physics_sha256": "962e7b84f47771bf616f3499d43e7e65fd8e8d1fb58e22760b32e4e6b90e6ac9",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.009042194694912317,
  "max_drift_m": 0.04832787779595598,
  "radial_IAE_m_s": 0.652919697478197,
  "signed_longitudinal_delta_m": -0.009035002114376623,
  "tail_speed_mean_m_s": 3.591324472731183e-05,
  "tail_speed_rms_m_s": 3.608714385298255e-05,
  "tail_sensor_speed_mean_m_s": 3.551831998495308e-05,
  "tail_fk_speed_mean_m_s": 3.7493514288954734e-05,
  "peak_tilt_rad": 0.11716786902187137,
  "peak_wheel_torque_nm": 1.1059315204620361,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.27674765550118097,
  "final_integral_m_s": 0.27674765550118097,
  "elapsed_wall_s": 9.579529824026395
}
```
