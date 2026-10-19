# tita_flash_sac_115632_883848_model_35000_com_minus5mm_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 04d8993b85810ece43a5d202a8a86b46097dcc9e30ce2c7825e73f538f9beab6

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_35000_com_minus5mm_baseline_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_35000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "com": -0.005
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
  "initial_physics_sha256": "7045fdedd39f6724cabf4544c66cc164a6ed4e4ebaf93c70091a0bec8c312bd7",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 12.841654616560879,
  "max_drift_m": 12.841654616560879,
  "radial_IAE_m_s": 381.0318840136039,
  "signed_longitudinal_delta_m": 12.840099952618955,
  "tail_speed_mean_m_s": 0.21717495813977022,
  "tail_speed_rms_m_s": 0.21717496038720016,
  "tail_sensor_speed_mean_m_s": 0.21670521438921028,
  "tail_fk_speed_mean_m_s": 0.21670292024923432,
  "peak_tilt_rad": 0.1384325543800886,
  "peak_wheel_torque_nm": 1.004075288772583,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.952006620005704
}
```
