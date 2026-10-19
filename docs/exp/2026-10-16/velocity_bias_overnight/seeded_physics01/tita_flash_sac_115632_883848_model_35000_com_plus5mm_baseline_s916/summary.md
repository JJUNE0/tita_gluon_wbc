# tita_flash_sac_115632_883848_model_35000_com_plus5mm_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 04d8993b85810ece43a5d202a8a86b46097dcc9e30ce2c7825e73f538f9beab6

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_35000_com_plus5mm_baseline_s916",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_35000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "com": 0.005
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
  "initial_physics_sha256": "57706da23b5260a8206bd99b8e58b9d79a2ad84f1338b9c77f5115177993d703",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 14.922279684775276,
  "max_drift_m": 14.922279684775276,
  "radial_IAE_m_s": 444.3711366558703,
  "signed_longitudinal_delta_m": 14.91817373993671,
  "tail_speed_mean_m_s": 0.25131188667513105,
  "tail_speed_rms_m_s": 0.25131189087994665,
  "tail_sensor_speed_mean_m_s": 0.25076819761866986,
  "tail_fk_speed_mean_m_s": 0.2507665434371687,
  "peak_tilt_rad": 0.14206729856684364,
  "peak_wheel_torque_nm": 0.7262573838233948,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 13.938657847989816
}
```
