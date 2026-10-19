# tita_flash_sac_115632_883848_model_10000_com_plus5mm_baseline_s913_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 48a0379d0b30385cff5ccfe473d0ee136f303e640a505719a82bad5a3e3178a5

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_10000_com_plus5mm_baseline_s913_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_10000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 913,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "com": 0.005
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "48a0379d0b30385cff5ccfe473d0ee136f303e640a505719a82bad5a3e3178a5",
  "onnx_sha256": "06e48800bb84c9f9275464d939d3614105bfbc1bbe6af1e92522c94faa5f1e15",
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
  "initial_physics_sha256": "aa9aa50f5f86e473cdfdf07313c4362dfa8aa8db6cf94ebc5345abfedb91261a",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 9.16512361769418,
  "max_drift_m": 9.16512361769418,
  "radial_IAE_m_s": 1397.628385309266,
  "signed_longitudinal_delta_m": 9.152995264043724,
  "tail_speed_mean_m_s": 0.029853533847693483,
  "tail_speed_rms_m_s": 0.032722006860360954,
  "tail_sensor_speed_mean_m_s": 0.028327163682193023,
  "tail_fk_speed_mean_m_s": 0.029584597613572697,
  "peak_tilt_rad": 0.12048872420111256,
  "peak_wheel_torque_nm": 3.1337149143218994,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 50.65672042599181
}
```
