# tita_flash_sac_115632_883848_model_40000_kick-0.2_baseline_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a4b5c15c3add7114e65d55cabbe505c0fffcd993df1b9162587e073cca97a891

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_40000_kick-0.2_baseline_s912",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_40000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 912,
    "estimator": "fk",
    "runtime": false,
    "kick": -0.2,
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
  "initial_physics_sha256": "8cffe3988f1e3662dfe1b4f5103512e3e3dcf352761124be83e74c0799e673fc",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 6.938879849039092,
  "max_drift_m": 6.938879849039092,
  "radial_IAE_m_s": 203.78251603362244,
  "signed_longitudinal_delta_m": 6.923119621001576,
  "tail_speed_mean_m_s": 0.11773221195841152,
  "tail_speed_rms_m_s": 0.1177325948832406,
  "tail_sensor_speed_mean_m_s": 0.11747757519078117,
  "tail_fk_speed_mean_m_s": 0.11747788318322465,
  "peak_tilt_rad": 0.11564248266607158,
  "peak_wheel_torque_nm": 1.8103946447372437,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.410903088981286
}
```
