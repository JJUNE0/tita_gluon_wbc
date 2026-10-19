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
  "initial_physics_sha256": "8fafdbc55603c6e52bee0c99e0346e19fea0f5e9af13304d3d2e09a5f2449fc4",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.015084123164052363,
  "max_drift_m": 0.15587480889386818,
  "radial_IAE_m_s": 1.2197842961830139,
  "signed_longitudinal_delta_m": 0.014978504660386681,
  "tail_speed_mean_m_s": -3.761384112152982e-05,
  "tail_speed_rms_m_s": 3.761716928442511e-05,
  "tail_sensor_speed_mean_m_s": -2.2987117633927788e-05,
  "tail_fk_speed_mean_m_s": -1.3508411192534217e-05,
  "peak_tilt_rad": 0.17526226608373818,
  "peak_wheel_torque_nm": 2.824289560317993,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.675900654717352,
  "final_integral_m_s": 0.675900654717352,
  "elapsed_wall_s": 9.554493953997735
}
```
