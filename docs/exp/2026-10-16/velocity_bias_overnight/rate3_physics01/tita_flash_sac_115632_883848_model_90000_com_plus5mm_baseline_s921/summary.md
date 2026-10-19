# tita_flash_sac_115632_883848_model_90000_com_plus5mm_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 4930085834f72c133d65563169762514342959361a6d71630216f5f608b0531f

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_90000_com_plus5mm_baseline_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_90000",
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
  "checkpoint_sha256": "4930085834f72c133d65563169762514342959361a6d71630216f5f608b0531f",
  "onnx_sha256": "1d6ffa5d91a15cf74e2abf755c367c1fb151f6e3c740618a6e1fb2fbf28f9379",
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
  "initial_physics_sha256": "ae0377aab6e2d35c3d0da1b4f273dfc36ac3b82d0b5381b33408580110844b0d",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 7.565194088402766,
  "max_drift_m": 7.565194088402766,
  "radial_IAE_m_s": 224.73004717882336,
  "signed_longitudinal_delta_m": 7.563795768931407,
  "tail_speed_mean_m_s": 0.12819972905547986,
  "tail_speed_rms_m_s": 0.1282001048588779,
  "tail_sensor_speed_mean_m_s": 0.12792228600339023,
  "tail_fk_speed_mean_m_s": 0.12792096365055236,
  "peak_tilt_rad": 0.07118938624071136,
  "peak_wheel_torque_nm": 0.19673562049865723,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 15.28880807000678
}
```
