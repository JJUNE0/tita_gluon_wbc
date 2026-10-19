# p011_tita_flash_sac_193248_068255_model_20000

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 4bb0e92e03390c3256497280f4ab3eda89d64ce8dfc23bfd9d799d69aa0d068c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "p011_tita_flash_sac_193248_068255_model_20000",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_20000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "analytic",
    "physics": {
      "mass": 1.3
    },
    "law": {
      "kp": 2.0,
      "ki": 15.0,
      "tau": 0.2,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0,
      "kp_fast": 4.0
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
  "initial_physics_sha256": "bb5de423d1bc5b38f9ad5544f877dc8ad7f955fb02a7c2ae6b556258a14811e9",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.5297118761103411,
  "max_drift_m": 0.6629600441455145,
  "radial_IAE_m_s": 15.308350762752248,
  "signed_longitudinal_delta_m": 0.5297095475122818,
  "tail_speed_mean_m_s": 0.012620402555600964,
  "tail_speed_rms_m_s": 0.1853944315118337,
  "tail_sensor_speed_mean_m_s": 0.012950362496082455,
  "tail_fk_speed_mean_m_s": 0.012645293873526593,
  "peak_tilt_rad": 0.3512996653597895,
  "peak_wheel_torque_nm": 2.0805928707122803,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -1.1535404820895276,
  "final_integral_m_s": -0.9348968415455421,
  "elapsed_wall_s": 19.398451549001038
}
```
