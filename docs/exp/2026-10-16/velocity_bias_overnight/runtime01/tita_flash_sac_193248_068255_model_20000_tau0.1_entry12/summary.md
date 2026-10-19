# tita_flash_sac_193248_068255_model_20000_tau0.1_entry12

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 4bb0e92e03390c3256497280f4ab3eda89d64ce8dfc23bfd9d799d69aa0d068c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_20000_tau0.1_entry12",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_20000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 271,
    "estimator": "fk",
    "runtime": true,
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.1,
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
  "final_drift_m": 0.06348579949637656,
  "max_drift_m": 0.08909150629829785,
  "radial_IAE_m_s": 3.866239750935149,
  "signed_longitudinal_delta_m": 0.06348514322468896,
  "tail_speed_mean_m_s": -3.061950143807793e-05,
  "tail_speed_rms_m_s": 3.062287809718491e-05,
  "tail_sensor_speed_mean_m_s": -1.5248306688597775e-05,
  "tail_fk_speed_mean_m_s": -5.505140527945088e-06,
  "peak_tilt_rad": 0.1513080148005086,
  "peak_wheel_torque_nm": 1.6480129957199097,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.6750733734567651,
  "final_integral_m_s": 0.6750844092710143,
  "elapsed_wall_s": 6.033642998023424
}
```
