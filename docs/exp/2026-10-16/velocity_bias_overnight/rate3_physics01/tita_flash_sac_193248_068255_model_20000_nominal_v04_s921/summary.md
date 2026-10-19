# tita_flash_sac_193248_068255_model_20000_nominal_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 4bb0e92e03390c3256497280f4ab3eda89d64ce8dfc23bfd9d799d69aa0d068c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_20000_nominal_v04_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_20000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": true,
    "physics": {},
    "law": {
      "kp": 0.0,
      "ki": 4.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 3.0,
      "seed_gain": 3.0
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
  "initial_physics_sha256": "980afb619459ab75c6dc361933b3923d25666c64cbc6d38c62c8fa0914381882",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.01316905347322411,
  "max_drift_m": 0.07576693580481218,
  "radial_IAE_m_s": 0.9425249053029722,
  "signed_longitudinal_delta_m": 0.013147763881408876,
  "tail_speed_mean_m_s": -3.98525940039251e-05,
  "tail_speed_rms_m_s": 3.985600893264174e-05,
  "tail_sensor_speed_mean_m_s": -2.3893691447399493e-05,
  "tail_fk_speed_mean_m_s": -1.3946035709803948e-05,
  "peak_tilt_rad": 0.1505399815246704,
  "peak_wheel_torque_nm": 1.8426029682159424,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.6744902357937443,
  "final_integral_m_s": 0.6744902357937443,
  "elapsed_wall_s": 7.305636189004872
}
```
