# tita_flash_sac_115632_883848_model_35000_friction08_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 04d8993b85810ece43a5d202a8a86b46097dcc9e30ce2c7825e73f538f9beab6

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_35000_friction08_baseline_s916",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_35000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "friction": 0.8
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
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
  "initial_physics_sha256": "7573e52813f0d46b3936ebfc55851c6acd6e2240b8c856ebd5a26a9cde1706d2",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 13.762184834219545,
  "max_drift_m": 13.762184834219545,
  "radial_IAE_m_s": 408.6631910605911,
  "signed_longitudinal_delta_m": 13.759302923263126,
  "tail_speed_mean_m_s": 0.23247898063506983,
  "tail_speed_rms_m_s": 0.23247898411253817,
  "tail_sensor_speed_mean_m_s": 0.23197606720422104,
  "tail_fk_speed_mean_m_s": 0.23197413200162836,
  "peak_tilt_rad": 0.14077208646611372,
  "peak_wheel_torque_nm": 0.9021746516227722,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 14.752593186974991
}
```
