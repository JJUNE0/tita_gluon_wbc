# tita_flash_sac_115632_883848_model_35000_v02_s911_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 04d8993b85810ece43a5d202a8a86b46097dcc9e30ce2c7825e73f538f9beab6

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_35000_v02_s911_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_35000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 911,
    "estimator": "fk",
    "runtime": true,
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
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
  "initial_physics_sha256": "2e48c85220bc942a9f7147f6b533098f487de30365af0fd046e66caa2b07ac87",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.05741789542729011,
  "max_drift_m": 0.07840192971747459,
  "radial_IAE_m_s": 17.310823020653913,
  "signed_longitudinal_delta_m": 0.05741446765719748,
  "tail_speed_mean_m_s": -1.3415778684860286e-05,
  "tail_speed_rms_m_s": 1.3471364156512523e-05,
  "tail_sensor_speed_mean_m_s": -1.2838813097251216e-05,
  "tail_fk_speed_mean_m_s": -1.0688711709455466e-05,
  "peak_tilt_rad": 0.13806323228492734,
  "peak_wheel_torque_nm": 1.2992640733718872,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.6078000676318139,
  "final_integral_m_s": 0.6078226992974208,
  "elapsed_wall_s": 55.30847118003294
}
```
