# tita_flash_sac_115632_883848_model_35000_com_minus5mm_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 04d8993b85810ece43a5d202a8a86b46097dcc9e30ce2c7825e73f538f9beab6

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_35000_com_minus5mm_baseline_s916",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_35000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "com": -0.005
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
  "initial_physics_sha256": "e3c81341d055a77aa34a5911cf39ff4d726f683f787d0aabbee18ffe97d4a6cf",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 12.828265563860917,
  "max_drift_m": 12.828265563860917,
  "radial_IAE_m_s": 380.31571721121657,
  "signed_longitudinal_delta_m": 12.827817694182585,
  "tail_speed_mean_m_s": 0.21717123955264644,
  "tail_speed_rms_m_s": 0.2171712420716846,
  "tail_sensor_speed_mean_m_s": 0.21670150027708812,
  "tail_fk_speed_mean_m_s": 0.21669921099416128,
  "peak_tilt_rad": 0.13851489449174692,
  "peak_wheel_torque_nm": 1.0163553953170776,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 12.709898308035918
}
```
