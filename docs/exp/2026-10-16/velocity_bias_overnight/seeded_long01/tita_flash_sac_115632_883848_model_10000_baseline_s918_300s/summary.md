# tita_flash_sac_115632_883848_model_10000_baseline_s918_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 48a0379d0b30385cff5ccfe473d0ee136f303e640a505719a82bad5a3e3178a5

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_10000_baseline_s918_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_10000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 918,
    "estimator": "fk",
    "guarded": false,
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
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
  "initial_physics_sha256": "48422e2724e3c0ac4bfc44896d94d3ed387a67243439ac944822ce49ca34e738",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 6.249584508799215,
  "max_drift_m": 6.249584508799215,
  "radial_IAE_m_s": 969.866123361832,
  "signed_longitudinal_delta_m": 6.224830890085959,
  "tail_speed_mean_m_s": 0.01981158013797744,
  "tail_speed_rms_m_s": 0.02220810396630355,
  "tail_sensor_speed_mean_m_s": 0.01870400075901159,
  "tail_fk_speed_mean_m_s": 0.019710331756449272,
  "peak_tilt_rad": 0.11507218681387799,
  "peak_wheel_torque_nm": 2.842644691467285,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 45.600808100018185
}
```
