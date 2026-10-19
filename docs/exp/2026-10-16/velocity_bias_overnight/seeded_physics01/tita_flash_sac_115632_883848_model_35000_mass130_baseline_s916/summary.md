# tita_flash_sac_115632_883848_model_35000_mass130_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 04d8993b85810ece43a5d202a8a86b46097dcc9e30ce2c7825e73f538f9beab6

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_35000_mass130_baseline_s916",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_35000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "mass": 1.3
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
  "initial_physics_sha256": "196e33413ef3c556a69e0dd71bd0e58d29e2d0da0c9599044376c766af6b0c8c",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 1.159359356860383,
  "max_drift_m": 1.159359356860383,
  "radial_IAE_m_s": 33.8102548184714,
  "signed_longitudinal_delta_m": 1.158643094834236,
  "tail_speed_mean_m_s": 0.020321073405040344,
  "tail_speed_rms_m_s": 0.020322508927808566,
  "tail_sensor_speed_mean_m_s": 0.020277413375805048,
  "tail_fk_speed_mean_m_s": 0.02027763632276911,
  "peak_tilt_rad": 0.122076678640614,
  "peak_wheel_torque_nm": 0.7105963826179504,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 12.773927417001687
}
```
