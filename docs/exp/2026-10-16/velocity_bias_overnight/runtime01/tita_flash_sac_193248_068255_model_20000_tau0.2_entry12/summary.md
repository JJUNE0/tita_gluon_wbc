# tita_flash_sac_193248_068255_model_20000_tau0.2_entry12

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 4bb0e92e03390c3256497280f4ab3eda89d64ce8dfc23bfd9d799d69aa0d068c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_20000_tau0.2_entry12",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_20000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 271,
    "estimator": "fk",
    "runtime": true,
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.2,
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
  "final_drift_m": 0.06349758900246869,
  "max_drift_m": 0.0923939017570677,
  "radial_IAE_m_s": 3.8692333274586974,
  "signed_longitudinal_delta_m": 0.06349687270527475,
  "tail_speed_mean_m_s": -3.061140804072252e-05,
  "tail_speed_rms_m_s": 3.061477257902765e-05,
  "tail_sensor_speed_mean_m_s": -1.524995391098079e-05,
  "tail_fk_speed_mean_m_s": -5.50961659902541e-06,
  "peak_tilt_rad": 0.15155329761258263,
  "peak_wheel_torque_nm": 1.563554286956787,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.6750826919365921,
  "final_integral_m_s": 0.6750938908685383,
  "elapsed_wall_s": 5.9849310189601965
}
```
