# tita_flash_sac_193248_068255_model_90000_kick+0.2_v03_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d94ec425dcab69bfb8001711468b6ca37297f4e1aec2e9b20535fd106ee98769

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_90000_kick+0.2_v03_s917",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_90000",
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
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
  },
  "checkpoint_sha256": "d94ec425dcab69bfb8001711468b6ca37297f4e1aec2e9b20535fd106ee98769",
  "onnx_sha256": "aff309a07b913000eb7916a9b3867232296f7834f48d5391c16e7ec4e09b84d2",
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
  "initial_physics_sha256": "2630df2e0f4a879459569daea5a98a62efd555d88fb15d8521e4c95fd70524c6",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.01073438373085239,
  "max_drift_m": 0.16460390631984578,
  "radial_IAE_m_s": 1.3539648678692906,
  "signed_longitudinal_delta_m": -0.010625612359979908,
  "tail_speed_mean_m_s": 0.00015921644420803174,
  "tail_speed_rms_m_s": 0.00016034972148750687,
  "tail_sensor_speed_mean_m_s": 0.00015914449679308354,
  "tail_fk_speed_mean_m_s": 0.00016054676446527246,
  "peak_tilt_rad": 0.11365643201127762,
  "peak_wheel_torque_nm": 1.3135406970977783,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.6410278133763392,
  "final_integral_m_s": 0.6410278133763392,
  "elapsed_wall_s": 14.268981027998962
}
```
