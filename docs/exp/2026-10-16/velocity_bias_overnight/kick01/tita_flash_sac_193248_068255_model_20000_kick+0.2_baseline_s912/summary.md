# tita_flash_sac_193248_068255_model_20000_kick+0.2_baseline_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 4bb0e92e03390c3256497280f4ab3eda89d64ce8dfc23bfd9d799d69aa0d068c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_20000_kick+0.2_baseline_s912",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_20000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 912,
    "estimator": "fk",
    "runtime": false,
    "kick": 0.2,
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
  "initial_physics_sha256": "5b15113a5ffcc82f90b81245aa128f137e71b9ac146c5b6ed70bf61f8a9ec601",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 13.125162250603092,
  "max_drift_m": 13.125162250603092,
  "radial_IAE_m_s": 396.55717419842244,
  "signed_longitudinal_delta_m": 13.088794527145874,
  "tail_speed_mean_m_s": 0.21848324899316945,
  "tail_speed_rms_m_s": 0.21848324902834815,
  "tail_sensor_speed_mean_m_s": 0.21801175772571801,
  "tail_fk_speed_mean_m_s": 0.21800184595261726,
  "peak_tilt_rad": 0.17865323860486115,
  "peak_wheel_torque_nm": 2.7675628662109375,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 12.917054001998622
}
```
