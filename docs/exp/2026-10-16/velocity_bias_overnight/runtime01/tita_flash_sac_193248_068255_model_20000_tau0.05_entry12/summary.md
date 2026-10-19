# tita_flash_sac_193248_068255_model_20000_tau0.05_entry12

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 4bb0e92e03390c3256497280f4ab3eda89d64ce8dfc23bfd9d799d69aa0d068c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_20000_tau0.05_entry12",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_20000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 271,
    "estimator": "fk",
    "runtime": true,
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.05,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
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
  "initial_physics_sha256": "051809db9c88e5f0ee6232bf82eac24f1188a0290d34eb09a4007280a6466a52",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.06347434210465663,
  "max_drift_m": 0.08703305570123387,
  "radial_IAE_m_s": 3.865023000743334,
  "signed_longitudinal_delta_m": 0.06347370549899609,
  "tail_speed_mean_m_s": -3.067363619714017e-05,
  "tail_speed_rms_m_s": 3.067693987474897e-05,
  "tail_sensor_speed_mean_m_s": -1.5261968251209043e-05,
  "tail_fk_speed_mean_m_s": -5.508241415722765e-06,
  "peak_tilt_rad": 0.15112855222063026,
  "peak_wheel_torque_nm": 1.6950114965438843,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.6750338868614961,
  "final_integral_m_s": 0.675044845114993,
  "elapsed_wall_s": 5.938531180960126
}
```
