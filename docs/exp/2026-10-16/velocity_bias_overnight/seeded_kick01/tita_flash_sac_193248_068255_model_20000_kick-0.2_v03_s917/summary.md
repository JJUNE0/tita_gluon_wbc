# tita_flash_sac_193248_068255_model_20000_kick-0.2_v03_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 4bb0e92e03390c3256497280f4ab3eda89d64ce8dfc23bfd9d799d69aa0d068c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_20000_kick-0.2_v03_s917",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_20000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 917,
    "estimator": "fk",
    "guarded": true,
    "kick": -0.2,
    "law": {
      "kp": 0.0,
      "ki": 4.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0,
      "seed_gain": 3.0
    },
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
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
  "initial_physics_sha256": "d4f4c238d53132f68a8618137ca7fbf12f04b1f59757e005353eeffb3ed80d96",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.006059819071529044,
  "max_drift_m": 0.013522811459446468,
  "radial_IAE_m_s": 0.2926348224384636,
  "signed_longitudinal_delta_m": -0.006049956510607388,
  "tail_speed_mean_m_s": -4.143303659642215e-05,
  "tail_speed_rms_m_s": 4.143633559513747e-05,
  "tail_sensor_speed_mean_m_s": -2.4545612073884143e-05,
  "tail_fk_speed_mean_m_s": -1.4242787244621063e-05,
  "peak_tilt_rad": 0.1463526827571462,
  "peak_wheel_torque_nm": 1.4764339923858643,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.6734769791957795,
  "final_integral_m_s": 0.6734769791957795,
  "elapsed_wall_s": 8.91281152603915
}
```
