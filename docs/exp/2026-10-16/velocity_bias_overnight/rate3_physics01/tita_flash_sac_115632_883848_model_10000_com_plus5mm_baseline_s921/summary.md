# tita_flash_sac_115632_883848_model_10000_com_plus5mm_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 48a0379d0b30385cff5ccfe473d0ee136f303e640a505719a82bad5a3e3178a5

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_10000_com_plus5mm_baseline_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_10000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "com": 0.005
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
  },
  "checkpoint_sha256": "48a0379d0b30385cff5ccfe473d0ee136f303e640a505719a82bad5a3e3178a5",
  "onnx_sha256": "06e48800bb84c9f9275464d939d3614105bfbc1bbe6af1e92522c94faa5f1e15",
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
  "initial_physics_sha256": "ca528a343e4a578557863a47eed724015af0f8f22201343ed0342dd3008629bd",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 1.9586611631144295,
  "max_drift_m": 1.9586611631144295,
  "radial_IAE_m_s": 60.056034269776816,
  "signed_longitudinal_delta_m": 1.957733468158121,
  "tail_speed_mean_m_s": 0.031258046819062066,
  "tail_speed_rms_m_s": 0.03410070898548529,
  "tail_sensor_speed_mean_m_s": 0.030578858731485335,
  "tail_fk_speed_mean_m_s": 0.03099342777130732,
  "peak_tilt_rad": 0.12048863109578112,
  "peak_wheel_torque_nm": 3.13374662399292,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 10.518132632016204
}
```
