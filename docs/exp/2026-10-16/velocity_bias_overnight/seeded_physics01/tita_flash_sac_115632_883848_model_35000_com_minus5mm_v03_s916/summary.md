# tita_flash_sac_115632_883848_model_35000_com_minus5mm_v03_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 04d8993b85810ece43a5d202a8a86b46097dcc9e30ce2c7825e73f538f9beab6

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_35000_com_minus5mm_v03_s916",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_35000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "com": -0.005
    },
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
  "initial_physics_sha256": "e3c81341d055a77aa34a5911cf39ff4d726f683f787d0aabbee18ffe97d4a6cf",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.024454501718828677,
  "max_drift_m": 0.0674240495764789,
  "radial_IAE_m_s": 1.4589059135660034,
  "signed_longitudinal_delta_m": 0.024451774679026792,
  "tail_speed_mean_m_s": 1.2668171399769867e-05,
  "tail_speed_rms_m_s": 1.2824132767572455e-05,
  "tail_sensor_speed_mean_m_s": 1.2460912943967185e-05,
  "tail_fk_speed_mean_m_s": 1.4815884716693418e-05,
  "peak_tilt_rad": 0.13548591937069454,
  "peak_wheel_torque_nm": 1.4938688278198242,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.5535836876388366,
  "final_integral_m_s": 0.5535836876388366,
  "elapsed_wall_s": 11.810705870040692
}
```
