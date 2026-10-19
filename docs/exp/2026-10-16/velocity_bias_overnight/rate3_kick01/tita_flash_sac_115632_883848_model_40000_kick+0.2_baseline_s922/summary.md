# tita_flash_sac_115632_883848_model_40000_kick+0.2_baseline_s922

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a4b5c15c3add7114e65d55cabbe505c0fffcd993df1b9162587e073cca97a891

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_40000_kick+0.2_baseline_s922",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_40000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 922,
    "estimator": "fk",
    "guarded": false,
    "kick": 0.2,
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
  "initial_physics_sha256": "0ba5b849aa315a918dbd61fa27a999f65e0c5c8d357dff5e0d0cce140a3d41d0",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 7.212148437290345,
  "max_drift_m": 7.212148437290345,
  "radial_IAE_m_s": 220.12576946221748,
  "signed_longitudinal_delta_m": 7.196925205817455,
  "tail_speed_mean_m_s": 0.117617439165047,
  "tail_speed_rms_m_s": 0.11761785842349162,
  "tail_sensor_speed_mean_m_s": 0.11736307650507374,
  "tail_fk_speed_mean_m_s": 0.11736334561619287,
  "peak_tilt_rad": 0.14546504047899944,
  "peak_wheel_torque_nm": 1.765362024307251,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.122742644976825
}
```
