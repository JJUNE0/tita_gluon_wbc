# tita_flash_sac_115632_883848_model_40000_com_minus5mm_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a4b5c15c3add7114e65d55cabbe505c0fffcd993df1b9162587e073cca97a891

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_40000_com_minus5mm_baseline_s916",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_40000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "com": -0.005
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
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
  "initial_physics_sha256": "a01c7b269dd8b71afcad228c73e25f7c3f0fca8fde65867ce8a539f59493523d",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 6.028824277400902,
  "max_drift_m": 6.028824277400902,
  "radial_IAE_m_s": 180.2659516347165,
  "signed_longitudinal_delta_m": 6.015588810595868,
  "tail_speed_mean_m_s": 0.10053491234154288,
  "tail_speed_rms_m_s": 0.10053497771323368,
  "tail_sensor_speed_mean_m_s": 0.10031769269636319,
  "tail_fk_speed_mean_m_s": 0.10031756197583404,
  "peak_tilt_rad": 0.11259099842005948,
  "peak_wheel_torque_nm": 0.29952937364578247,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 13.693031977978535
}
```
