# tita_flash_sac_193248_068255_model_20000_kick+0.2_v03_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 4bb0e92e03390c3256497280f4ab3eda89d64ce8dfc23bfd9d799d69aa0d068c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_20000_kick+0.2_v03_s917",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_20000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 917,
    "estimator": "fk",
    "guarded": true,
    "kick": 0.2,
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
  "initial_physics_sha256": "8fafdbc55603c6e52bee0c99e0346e19fea0f5e9af13304d3d2e09a5f2449fc4",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.0032293833462485677,
  "max_drift_m": 0.15529196396511,
  "radial_IAE_m_s": 0.4201621973567309,
  "signed_longitudinal_delta_m": -0.0025770824103097485,
  "tail_speed_mean_m_s": -3.745814536156441e-05,
  "tail_speed_rms_m_s": 3.746159705328967e-05,
  "tail_sensor_speed_mean_m_s": -2.2928161153972702e-05,
  "tail_fk_speed_mean_m_s": -1.347974340515436e-05,
  "peak_tilt_rad": 0.17515521891467523,
  "peak_wheel_torque_nm": 2.831071615219116,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.6759967018117229,
  "final_integral_m_s": 0.6759967018117229,
  "elapsed_wall_s": 8.8596768300049
}
```
