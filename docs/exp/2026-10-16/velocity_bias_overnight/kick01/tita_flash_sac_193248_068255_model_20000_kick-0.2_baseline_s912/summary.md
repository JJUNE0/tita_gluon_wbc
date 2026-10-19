# tita_flash_sac_193248_068255_model_20000_kick-0.2_baseline_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 4bb0e92e03390c3256497280f4ab3eda89d64ce8dfc23bfd9d799d69aa0d068c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_20000_kick-0.2_baseline_s912",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_20000",
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
  "checkpoint_sha256": "4bb0e92e03390c3256497280f4ab3eda89d64ce8dfc23bfd9d799d69aa0d068c",
  "onnx_sha256": "a24d51f2c61ac25fc44c8e657cd90494575b17855d820a382e66b027caddbaac",
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
  "initial_physics_sha256": "1ec06f932cb130c1bd860eaf26cbde5845728a6087f175f27a7e1c98391bf687",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 12.93141005188791,
  "max_drift_m": 12.93141005188791,
  "radial_IAE_m_s": 384.9251759279192,
  "signed_longitudinal_delta_m": 12.900730903811825,
  "tail_speed_mean_m_s": 0.2184824513764184,
  "tail_speed_rms_m_s": 0.21848245142123857,
  "tail_sensor_speed_mean_m_s": 0.21801100544372007,
  "tail_fk_speed_mean_m_s": 0.21800104998500747,
  "peak_tilt_rad": 0.1595553878373741,
  "peak_wheel_torque_nm": 1.5429377555847168,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 10.784477375040296
}
```
