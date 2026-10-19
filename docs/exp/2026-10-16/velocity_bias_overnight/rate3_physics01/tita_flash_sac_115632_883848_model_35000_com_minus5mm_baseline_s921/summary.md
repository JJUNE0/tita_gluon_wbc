# tita_flash_sac_115632_883848_model_35000_com_minus5mm_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 04d8993b85810ece43a5d202a8a86b46097dcc9e30ce2c7825e73f538f9beab6

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_35000_com_minus5mm_baseline_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_35000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "com": -0.005
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
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
  "initial_physics_sha256": "e641c9374af1a2f88da63e83368116b96064f0ec0e5c258641d4dffc8136b310",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 12.841653973185805,
  "max_drift_m": 12.841653973185805,
  "radial_IAE_m_s": 381.0318778963137,
  "signed_longitudinal_delta_m": 12.840099304393272,
  "tail_speed_mean_m_s": 0.2171749285776411,
  "tail_speed_rms_m_s": 0.21717493082504388,
  "tail_sensor_speed_mean_m_s": 0.21670518080872064,
  "tail_fk_speed_mean_m_s": 0.21670289105184867,
  "peak_tilt_rad": 0.13843251621127273,
  "peak_wheel_torque_nm": 1.0040827989578247,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 10.087473050982226
}
```
