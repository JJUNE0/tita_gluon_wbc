# tita_flash_sac_115632_883848_model_40000_friction08_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a4b5c15c3add7114e65d55cabbe505c0fffcd993df1b9162587e073cca97a891

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_40000_friction08_baseline_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_40000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "friction": 0.8
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
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
  "final_drift_m": 7.087573649183402,
  "max_drift_m": 7.087573649183402,
  "radial_IAE_m_s": 212.29353842852856,
  "signed_longitudinal_delta_m": 7.040353595889827,
  "tail_speed_mean_m_s": 0.1180275233938114,
  "tail_speed_rms_m_s": 0.11802793258922857,
  "tail_sensor_speed_mean_m_s": 0.11777217575635922,
  "tail_fk_speed_mean_m_s": 0.1177726141992184,
  "peak_tilt_rad": 0.11656321098791911,
  "peak_wheel_torque_nm": 0.3139057159423828,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 7.478168884001207
}
```
