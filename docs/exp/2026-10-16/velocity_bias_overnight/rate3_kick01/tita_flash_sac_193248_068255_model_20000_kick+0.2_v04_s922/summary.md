# tita_flash_sac_193248_068255_model_20000_kick+0.2_v04_s922

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 4bb0e92e03390c3256497280f4ab3eda89d64ce8dfc23bfd9d799d69aa0d068c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_20000_kick+0.2_v04_s922",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_20000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 922,
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
  "initial_physics_sha256": "21969d78aecabf3fad1bdb69979fcb47e029599389e8bc8d6d8e2f5642850a7b",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.0152278586475986,
  "max_drift_m": 0.14096265594190074,
  "radial_IAE_m_s": 1.1782926793251147,
  "signed_longitudinal_delta_m": 0.015154423021828093,
  "tail_speed_mean_m_s": -3.6755491401748445e-05,
  "tail_speed_rms_m_s": 3.6758741236024636e-05,
  "tail_sensor_speed_mean_m_s": -2.2655072601319978e-05,
  "tail_fk_speed_mean_m_s": -1.3351493530369558e-05,
  "peak_tilt_rad": 0.1746988321936136,
  "peak_wheel_torque_nm": 2.8281030654907227,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.676445594015392,
  "final_integral_m_s": 0.676445594015392,
  "elapsed_wall_s": 7.192034844018053
}
```
