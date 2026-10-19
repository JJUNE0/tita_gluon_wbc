# tita_flash_sac_193248_068255_model_20000_friction08_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 4bb0e92e03390c3256497280f4ab3eda89d64ce8dfc23bfd9d799d69aa0d068c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_20000_friction08_baseline_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_20000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "friction": 0.8
    },
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
  "initial_physics_sha256": "c674fdf1ee4b972ba6969b94fb5e0ca70015217d7acaca2fa1f634ab12ca1a2b",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 13.030927387073618,
  "max_drift_m": 13.030927387073618,
  "radial_IAE_m_s": 390.66017096693827,
  "signed_longitudinal_delta_m": 13.023739351678403,
  "tail_speed_mean_m_s": 0.21848154093713756,
  "tail_speed_rms_m_s": 0.2184815409928311,
  "tail_sensor_speed_mean_m_s": 0.21801009699519802,
  "tail_fk_speed_mean_m_s": 0.21800013967900794,
  "peak_tilt_rad": 0.15955376693141643,
  "peak_wheel_torque_nm": 0.4046279191970825,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 11.58938775403658
}
```
