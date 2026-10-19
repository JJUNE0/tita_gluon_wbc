# tita_flash_sac_193248_068255_model_30000_kick-0.2_v03_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 1e8eb8c4549e7335f4ef3d31ec9b7b45fd0cb148283a41b8c616f429cefb643f

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_30000_kick-0.2_v03_s917",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_30000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 917,
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
  "initial_physics_sha256": "4d6b4bd7574a7e01cfa2e527cd8f17a9338a491923482f444f69ba88dc4ed716",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.03565157934601242,
  "max_drift_m": 0.07699941196742864,
  "radial_IAE_m_s": 2.1649771094007626,
  "signed_longitudinal_delta_m": -0.03565041792986699,
  "tail_speed_mean_m_s": -7.587879186632442e-06,
  "tail_speed_rms_m_s": 1.1369170868724359e-05,
  "tail_sensor_speed_mean_m_s": -7.330529167484356e-06,
  "tail_fk_speed_mean_m_s": -7.641196640147437e-06,
  "peak_tilt_rad": 0.030985919494284753,
  "peak_wheel_torque_nm": 1.2806274890899658,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.11021340730698752,
  "final_integral_m_s": 0.11021340730698752,
  "elapsed_wall_s": 8.8870273270295
}
```
