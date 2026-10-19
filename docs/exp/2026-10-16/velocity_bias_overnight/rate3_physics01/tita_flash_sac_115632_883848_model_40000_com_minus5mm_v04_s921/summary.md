# tita_flash_sac_115632_883848_model_40000_com_minus5mm_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a4b5c15c3add7114e65d55cabbe505c0fffcd993df1b9162587e073cca97a891

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_40000_com_minus5mm_v04_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_40000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "com": -0.005
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
  "initial_physics_sha256": "edb5fa1c5d57c2673b764fb3ebea1e7a6994ba2538784f9025493ac3e1c42d07",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.002515420936124085,
  "max_drift_m": 0.031756058968803284,
  "radial_IAE_m_s": 0.11468960472174998,
  "signed_longitudinal_delta_m": 0.002419157502035733,
  "tail_speed_mean_m_s": 4.924569884041043e-05,
  "tail_speed_rms_m_s": 4.931298073260024e-05,
  "tail_sensor_speed_mean_m_s": 4.8472436540834805e-05,
  "tail_fk_speed_mean_m_s": 5.1136801778235506e-05,
  "peak_tilt_rad": 0.10897386673443821,
  "peak_wheel_torque_nm": 0.6850954294204712,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.19579238841842297,
  "final_integral_m_s": 0.19579238841842297,
  "elapsed_wall_s": 9.815817902970593
}
```
