# tita_flash_sac_115632_883848_model_35000_mass115_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 04d8993b85810ece43a5d202a8a86b46097dcc9e30ce2c7825e73f538f9beab6

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_35000_mass115_baseline_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_35000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "mass": 1.15
    },
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
  "initial_physics_sha256": "e06394447c512896d988591a197bb140f4516a902afe4ec60271beb14a7fd97b",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 8.379714874480673,
  "max_drift_m": 8.379714874480673,
  "radial_IAE_m_s": 249.73948856513545,
  "signed_longitudinal_delta_m": 8.379314970735892,
  "tail_speed_mean_m_s": 0.14094266712166356,
  "tail_speed_rms_m_s": 0.14094269118753375,
  "tail_sensor_speed_mean_m_s": 0.1406387786056548,
  "tail_fk_speed_mean_m_s": 0.14063880759871542,
  "peak_tilt_rad": 0.13890532265295152,
  "peak_wheel_torque_nm": 0.7542521357536316,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.223706282966305
}
```
