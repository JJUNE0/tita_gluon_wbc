# tita_flash_sac_193248_068255_model_30000_v03_s918_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 1e8eb8c4549e7335f4ef3d31ec9b7b45fd0cb148283a41b8c616f429cefb643f

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_30000_v03_s918_300s",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_30000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 918,
    "estimator": "fk",
    "guarded": true,
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
  "checkpoint_sha256": "1e8eb8c4549e7335f4ef3d31ec9b7b45fd0cb148283a41b8c616f429cefb643f",
  "onnx_sha256": "ec18f72b80fd3755cb0dce2de3434e16c4375a38100a8a08c28560539614d4a8",
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
  "initial_physics_sha256": "027b3f489c517f40bc553f1914833e65f8d1b15410d44aafa201d516bb74b079",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.009815974316687414,
  "max_drift_m": 0.01706480739528391,
  "radial_IAE_m_s": 2.852046911268965,
  "signed_longitudinal_delta_m": -0.009815973804816115,
  "tail_speed_mean_m_s": 5.481891026227385e-06,
  "tail_speed_rms_m_s": 5.482095232863913e-06,
  "tail_sensor_speed_mean_m_s": 5.497811473642181e-06,
  "tail_fk_speed_mean_m_s": 5.4527651954092115e-06,
  "peak_tilt_rad": 0.023481864700354516,
  "peak_wheel_torque_nm": 0.37976163625717163,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.10511812438779808,
  "final_integral_m_s": 0.10511812438779808,
  "elapsed_wall_s": 54.16781027201796
}
```
