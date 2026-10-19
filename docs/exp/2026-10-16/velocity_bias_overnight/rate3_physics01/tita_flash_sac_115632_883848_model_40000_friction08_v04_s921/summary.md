# tita_flash_sac_115632_883848_model_40000_friction08_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a4b5c15c3add7114e65d55cabbe505c0fffcd993df1b9162587e073cca97a891

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_40000_friction08_v04_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_40000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "friction": 0.8
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
  "initial_physics_sha256": "f83d2b161f0e5f6725b1c6ef3c232ab2d739e6f66b80dbce6d9a921908df011e",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.004625646927828703,
  "max_drift_m": 0.03920931378851241,
  "radial_IAE_m_s": 0.397706256817184,
  "signed_longitudinal_delta_m": -0.004625607454387808,
  "tail_speed_mean_m_s": 4.650970658692962e-05,
  "tail_speed_rms_m_s": 4.672476243254967e-05,
  "tail_sensor_speed_mean_m_s": 4.823677817767625e-05,
  "tail_fk_speed_mean_m_s": 5.088213999623544e-05,
  "peak_tilt_rad": 0.11383314959069524,
  "peak_wheel_torque_nm": 0.860237717628479,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.22939614223560625,
  "final_integral_m_s": 0.22939614223560625,
  "elapsed_wall_s": 9.71908974199323
}
```
