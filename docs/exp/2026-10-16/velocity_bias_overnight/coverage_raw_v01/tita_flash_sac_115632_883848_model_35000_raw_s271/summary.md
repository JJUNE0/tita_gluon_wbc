# tita_flash_sac_115632_883848_model_35000_raw_s271

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 04d8993b85810ece43a5d202a8a86b46097dcc9e30ce2c7825e73f538f9beab6

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_35000_raw_s271",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_35000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 271,
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.05,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
    },
    "estimator": "raw"
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
  "initial_physics_sha256": "e62d0332d89b35c67ef891d7dd3ee42dbdb39adaac22d10c2a375db21c7fa2f5",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.05743039560316579,
  "max_drift_m": 0.10229893853581487,
  "radial_IAE_m_s": 3.415162979597857,
  "signed_longitudinal_delta_m": 0.05741542559515731,
  "tail_speed_mean_m_s": 5.594316501943538e-05,
  "tail_speed_rms_m_s": 0.012346959160028505,
  "tail_sensor_speed_mean_m_s": 0.0008190761423688516,
  "tail_fk_speed_mean_m_s": 9.577962106252074e-05,
  "peak_tilt_rad": 0.13847770763121225,
  "peak_wheel_torque_nm": 1.506099820137024,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.7665231462885287,
  "final_integral_m_s": 0.7284414972951798,
  "elapsed_wall_s": 4.4469039349933155
}
```
