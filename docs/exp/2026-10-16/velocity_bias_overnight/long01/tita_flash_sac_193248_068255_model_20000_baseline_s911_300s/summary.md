# tita_flash_sac_193248_068255_model_20000_baseline_s911_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 4bb0e92e03390c3256497280f4ab3eda89d64ce8dfc23bfd9d799d69aa0d068c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_20000_baseline_s911_300s",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_20000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 911,
    "estimator": "fk",
    "runtime": false,
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
  "initial_physics_sha256": "4891bf645a774fa1dd23b6b263393877a393381596f4eb091be10c058156a8f2",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 58.329654867043644,
  "max_drift_m": 58.329654867043644,
  "radial_IAE_m_s": 9284.547805051541,
  "signed_longitudinal_delta_m": 43.53791802770054,
  "tail_speed_mean_m_s": 0.2184890354636365,
  "tail_speed_rms_m_s": 0.21848903546450313,
  "tail_sensor_speed_mean_m_s": 0.21801746719415668,
  "tail_fk_speed_mean_m_s": 0.21800762512511737,
  "peak_tilt_rad": 0.15956647840326288,
  "peak_wheel_torque_nm": 0.40890252590179443,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 43.25229916104581
}
```
