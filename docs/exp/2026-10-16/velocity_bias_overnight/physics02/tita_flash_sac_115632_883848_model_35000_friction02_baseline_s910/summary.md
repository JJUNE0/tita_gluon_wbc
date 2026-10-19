# tita_flash_sac_115632_883848_model_35000_friction02_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 04d8993b85810ece43a5d202a8a86b46097dcc9e30ce2c7825e73f538f9beab6

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_35000_friction02_baseline_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_35000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "friction": 0.2
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
  "initial_physics_sha256": "0a74cc9d897c66bbe41636929fc7a0a404444d245b6291a6a0f8714c2a0c806c",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 13.707614185011302,
  "max_drift_m": 13.707614185011302,
  "radial_IAE_m_s": 414.24390594346863,
  "signed_longitudinal_delta_m": 13.082750009152441,
  "tail_speed_mean_m_s": 0.23186041403228805,
  "tail_speed_rms_m_s": 0.231860414536075,
  "tail_sensor_speed_mean_m_s": 0.23155591587677338,
  "tail_fk_speed_mean_m_s": 0.23156358409637104,
  "peak_tilt_rad": 0.1370525340169899,
  "peak_wheel_torque_nm": 0.7657991647720337,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.492600733006839
}
```
