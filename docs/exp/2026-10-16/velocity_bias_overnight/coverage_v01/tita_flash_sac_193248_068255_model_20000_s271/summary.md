# tita_flash_sac_193248_068255_model_20000_s271

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 4bb0e92e03390c3256497280f4ab3eda89d64ce8dfc23bfd9d799d69aa0d068c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_20000_s271",
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
    "estimator": "fk"
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
  "final_drift_m": 0.06537155659121846,
  "max_drift_m": 0.09132072243184544,
  "radial_IAE_m_s": 3.9504137271680477,
  "signed_longitudinal_delta_m": 0.0653701322312698,
  "tail_speed_mean_m_s": -1.3050414233856487e-05,
  "tail_speed_rms_m_s": 1.3055188517986392e-05,
  "tail_sensor_speed_mean_m_s": -1.0808044385538343e-05,
  "tail_fk_speed_mean_m_s": -4.411593070111596e-06,
  "peak_tilt_rad": 0.15570494420032044,
  "peak_wheel_torque_nm": 1.7270008325576782,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.6877006753709833,
  "final_integral_m_s": 0.6877094421970394,
  "elapsed_wall_s": 4.546828572987579
}
```
