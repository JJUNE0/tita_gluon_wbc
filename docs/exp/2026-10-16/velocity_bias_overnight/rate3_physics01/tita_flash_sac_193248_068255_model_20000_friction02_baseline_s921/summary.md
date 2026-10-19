# tita_flash_sac_193248_068255_model_20000_friction02_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 4bb0e92e03390c3256497280f4ab3eda89d64ce8dfc23bfd9d799d69aa0d068c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_20000_friction02_baseline_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_20000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "friction": 0.2
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
  },
  "checkpoint_sha256": "4bb0e92e03390c3256497280f4ab3eda89d64ce8dfc23bfd9d799d69aa0d068c",
  "onnx_sha256": "a24d51f2c61ac25fc44c8e657cd90494575b17855d820a382e66b027caddbaac",
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
  "initial_physics_sha256": "aa7fff271c43db1099c898fcb347e4143e5e9c27f168f447f8a7d52bc4c66691",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 7.787563467462732,
  "max_drift_m": 7.787563467462732,
  "radial_IAE_m_s": 296.77392655592485,
  "signed_longitudinal_delta_m": -1.4654595238762633,
  "tail_speed_mean_m_s": 0.2082799970000708,
  "tail_speed_rms_m_s": 0.20827999703911107,
  "tail_sensor_speed_mean_m_s": 0.20869130929140187,
  "tail_fk_speed_mean_m_s": 0.2087761946422876,
  "peak_tilt_rad": 0.15306788225601076,
  "peak_wheel_torque_nm": 0.10177719593048096,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 7.903957745002117
}
```
