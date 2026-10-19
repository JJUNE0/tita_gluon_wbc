# tita_flash_sac_115632_883848_model_40000_kick-0.2_v04_s922

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a4b5c15c3add7114e65d55cabbe505c0fffcd993df1b9162587e073cca97a891

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_40000_kick-0.2_v04_s922",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_40000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 922,
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
  "initial_physics_sha256": "8dcbe3734235b8fa63d938fbf120e7942c35341265e20a04554c4b087ac4385b",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.006148552711193837,
  "max_drift_m": 0.040554214682734464,
  "radial_IAE_m_s": 0.4771396683031782,
  "signed_longitudinal_delta_m": -0.006128610988620763,
  "tail_speed_mean_m_s": 4.3459392695584016e-05,
  "tail_speed_rms_m_s": 4.356578855313006e-05,
  "tail_sensor_speed_mean_m_s": 4.286208108750249e-05,
  "tail_fk_speed_mean_m_s": 4.5228436864932936e-05,
  "peak_tilt_rad": 0.11290349872588457,
  "peak_wheel_torque_nm": 1.7327823638916016,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.2337810974175376,
  "final_integral_m_s": 0.2337810974175376,
  "elapsed_wall_s": 9.176653832022566
}
```
