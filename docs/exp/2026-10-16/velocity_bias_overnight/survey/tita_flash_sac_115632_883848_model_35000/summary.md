# tita_flash_sac_115632_883848_model_35000

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 04d8993b85810ece43a5d202a8a86b46097dcc9e30ce2c7825e73f538f9beab6

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_35000",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_35000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 270,
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "04d8993b85810ece43a5d202a8a86b46097dcc9e30ce2c7825e73f538f9beab6",
  "onnx_sha256": "3ce2f1cc7a17e8f712ba06efe9dc56bd55d6b0090b07942bae3238a59fef56e0",
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
  "initial_physics_sha256": "ccf541e72da3f2398cd93aafde680c9f80b53809f40f8ad09cecf8d67653693d",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 13.895353832557118,
  "max_drift_m": 13.895353832557118,
  "radial_IAE_m_s": 416.0790972563628,
  "signed_longitudinal_delta_m": 13.86954660280475,
  "tail_speed_mean_m_s": 0.23251899546628052,
  "tail_speed_rms_m_s": 0.23251899619646949,
  "tail_sensor_speed_mean_m_s": 0.2320159958850563,
  "tail_fk_speed_mean_m_s": 0.2320140514940834,
  "peak_tilt_rad": 0.13847769694242218,
  "peak_wheel_torque_nm": 0.15153849124908447,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 4.52502145699691
}
```
