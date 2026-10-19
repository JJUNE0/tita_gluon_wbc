# tita_flash_sac_115632_883848_model_35000_kick+0.2_v03_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 04d8993b85810ece43a5d202a8a86b46097dcc9e30ce2c7825e73f538f9beab6

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_35000_kick+0.2_v03_s917",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_35000",
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
  "checkpoint_sha256": "04d8993b85810ece43a5d202a8a86b46097dcc9e30ce2c7825e73f538f9beab6",
  "onnx_sha256": "3ce2f1cc7a17e8f712ba06efe9dc56bd55d6b0090b07942bae3238a59fef56e0",
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
  "initial_physics_sha256": "ee615353956b4b4df5e3141c9a255157782b1926bd8a92db684b5e5de47c87eb",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.09529726814601984,
  "max_drift_m": 0.1708668988766437,
  "radial_IAE_m_s": 5.71318524236296,
  "signed_longitudinal_delta_m": 0.09529724059919947,
  "tail_speed_mean_m_s": 4.7021655369669594e-05,
  "tail_speed_rms_m_s": 4.7419480828307963e-05,
  "tail_sensor_speed_mean_m_s": 4.689256497795578e-05,
  "tail_fk_speed_mean_m_s": 4.906158610258341e-05,
  "peak_tilt_rad": 0.16509332283821543,
  "peak_wheel_torque_nm": 3.1681251525878906,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.6025016357689597,
  "final_integral_m_s": 0.6025016357689597,
  "elapsed_wall_s": 9.667373711010441
}
```
