# tita_flash_sac_193248_068255_model_20000_kick-0.2_v04_s922

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 4bb0e92e03390c3256497280f4ab3eda89d64ce8dfc23bfd9d799d69aa0d068c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_20000_kick-0.2_v04_s922",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_20000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 922,
    "estimator": "fk",
    "guarded": true,
    "kick": -0.2,
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
  "initial_physics_sha256": "ad2455de9387d738726eb8ef3d60ba9d9967529f78fa4ce1ae62b3b57329ae52",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.011655159018238142,
  "max_drift_m": 0.01383965073485711,
  "radial_IAE_m_s": 0.7558474559728738,
  "signed_longitudinal_delta_m": 0.011653606043890385,
  "tail_speed_mean_m_s": -4.066028871074723e-05,
  "tail_speed_rms_m_s": 4.066359394918483e-05,
  "tail_sensor_speed_mean_m_s": -2.4222714998502644e-05,
  "tail_fk_speed_mean_m_s": -1.4097154318512056e-05,
  "peak_tilt_rad": 0.146486936307632,
  "peak_wheel_torque_nm": 1.4828720092773438,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.6739732231429255,
  "final_integral_m_s": 0.6739732231429255,
  "elapsed_wall_s": 8.465801784012001
}
```
