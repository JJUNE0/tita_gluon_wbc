# tita_flash_sac_193248_068255_model_20000_nominal_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 4bb0e92e03390c3256497280f4ab3eda89d64ce8dfc23bfd9d799d69aa0d068c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_20000_nominal_baseline_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_20000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {},
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
  "initial_physics_sha256": "6371b77413a2f123990b869b7b4f42921a808f25598f35d34a5ca6b8a43a5688",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 13.033747775603867,
  "max_drift_m": 13.033747775603867,
  "radial_IAE_m_s": 391.0718727471018,
  "signed_longitudinal_delta_m": 12.998633419939079,
  "tail_speed_mean_m_s": 0.21848297091620414,
  "tail_speed_rms_m_s": 0.21848297095432112,
  "tail_sensor_speed_mean_m_s": 0.2180115095406803,
  "tail_fk_speed_mean_m_s": 0.21800156841664614,
  "peak_tilt_rad": 0.159556141185919,
  "peak_wheel_torque_nm": 0.40906214714050293,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 15.594213319011033
}
```
