# tita_flash_sac_193248_068255_model_20000_kick+0.2_v02_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 4bb0e92e03390c3256497280f4ab3eda89d64ce8dfc23bfd9d799d69aa0d068c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_20000_kick+0.2_v02_s912",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_20000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 912,
    "estimator": "fk",
    "runtime": true,
    "kick": 0.2,
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
  "initial_physics_sha256": "5b15113a5ffcc82f90b81245aa128f137e71b9ac146c5b6ed70bf61f8a9ec601",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.06513828537893018,
  "max_drift_m": 0.1580826839884006,
  "radial_IAE_m_s": 4.044691324942657,
  "signed_longitudinal_delta_m": 0.06513286670977976,
  "tail_speed_mean_m_s": -2.8451388023769602e-05,
  "tail_speed_rms_m_s": 2.8454767774367956e-05,
  "tail_sensor_speed_mean_m_s": -1.4563554568684671e-05,
  "tail_fk_speed_mean_m_s": -5.322224947213684e-06,
  "peak_tilt_rad": 0.1758449527842758,
  "peak_wheel_torque_nm": 2.7894210815429688,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.6811693007025897,
  "final_integral_m_s": 0.6811802161705933,
  "elapsed_wall_s": 16.102740926027764
}
```
