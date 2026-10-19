# tita_flash_sac_193248_068255_model_30000_kick+0.2_v02_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 1e8eb8c4549e7335f4ef3d31ec9b7b45fd0cb148283a41b8c616f429cefb643f

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_30000_kick+0.2_v02_s912",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_30000",
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
  "checkpoint_sha256": "1e8eb8c4549e7335f4ef3d31ec9b7b45fd0cb148283a41b8c616f429cefb643f",
  "onnx_sha256": "ec18f72b80fd3755cb0dce2de3434e16c4375a38100a8a08c28560539614d4a8",
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
  "initial_physics_sha256": "67739eb934ab254fa33caf3f22177590faa07536824838fc653d17c4780b91c0",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.011725830555820058,
  "max_drift_m": 0.08251881231035307,
  "radial_IAE_m_s": 0.7555997080508112,
  "signed_longitudinal_delta_m": 0.011719208250378107,
  "tail_speed_mean_m_s": -7.133410253674871e-06,
  "tail_speed_rms_m_s": 7.428899186704642e-06,
  "tail_sensor_speed_mean_m_s": -6.8856306115179166e-06,
  "tail_fk_speed_mean_m_s": -7.186024491873868e-06,
  "peak_tilt_rad": 0.10270978147172771,
  "peak_wheel_torque_nm": 1.7010746002197266,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.11596412576059786,
  "final_integral_m_s": 0.11597960214966704,
  "elapsed_wall_s": 14.44281078298809
}
```
