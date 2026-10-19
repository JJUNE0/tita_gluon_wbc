# tita_flash_sac_193248_068255_model_30000_kick-0.2_baseline_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 1e8eb8c4549e7335f4ef3d31ec9b7b45fd0cb148283a41b8c616f429cefb643f

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_30000_kick-0.2_baseline_s912",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_30000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 912,
    "estimator": "fk",
    "runtime": false,
    "kick": -0.2,
    "law": {
      "mode": "constant",
      "bias": 0.0
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
  "initial_physics_sha256": "81c481fb12a9f7f3260f60f2508ea98f1ed3ffc56b73e9217cf2a340088be105",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 2.802983623777515,
  "max_drift_m": 2.802983623777515,
  "radial_IAE_m_s": 80.82778973555365,
  "signed_longitudinal_delta_m": 2.80214363949848,
  "tail_speed_mean_m_s": 0.048456326588729746,
  "tail_speed_rms_m_s": 0.04845651496344615,
  "tail_sensor_speed_mean_m_s": 0.04835106520271662,
  "tail_fk_speed_mean_m_s": 0.04834981710504755,
  "peak_tilt_rad": 0.02294609502492939,
  "peak_wheel_torque_nm": 1.337374210357666,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.791841904981993
}
```
