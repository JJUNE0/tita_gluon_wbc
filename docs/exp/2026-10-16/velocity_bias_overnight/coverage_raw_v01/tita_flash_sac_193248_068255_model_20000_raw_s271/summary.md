# tita_flash_sac_193248_068255_model_20000_raw_s271

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 4bb0e92e03390c3256497280f4ab3eda89d64ce8dfc23bfd9d799d69aa0d068c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_20000_raw_s271",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_20000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 271,
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.05,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
    },
    "estimator": "raw"
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
  "initial_physics_sha256": "7fc1e566d5e845eddd44ee39634172eeaf6c432820f06760060afd6ad12256f7",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.04857928133348468,
  "max_drift_m": 0.09124081275969838,
  "radial_IAE_m_s": 3.1129285112587053,
  "signed_longitudinal_delta_m": 0.04853329102589934,
  "tail_speed_mean_m_s": -0.0004880509159428828,
  "tail_speed_rms_m_s": 0.053884087909449846,
  "tail_sensor_speed_mean_m_s": -0.0001993255446364776,
  "tail_fk_speed_mean_m_s": -9.783107050388739e-05,
  "peak_tilt_rad": 0.15570494420032044,
  "peak_wheel_torque_nm": 2.140439987182617,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.7484463048602502,
  "final_integral_m_s": 0.6891166177102709,
  "elapsed_wall_s": 4.443823657988105
}
```
