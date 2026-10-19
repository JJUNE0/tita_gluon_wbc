# tita_flash_sac_115632_883848_model_35000_baseline_s911_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 04d8993b85810ece43a5d202a8a86b46097dcc9e30ce2c7825e73f538f9beab6

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_35000_baseline_s911_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_35000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 911,
    "estimator": "fk",
    "runtime": false,
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
  "initial_physics_sha256": "2e48c85220bc942a9f7147f6b533098f487de30365af0fd046e66caa2b07ac87",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 68.17008852575123,
  "max_drift_m": 68.17008852575123,
  "radial_IAE_m_s": 10313.927936624947,
  "signed_longitudinal_delta_m": 65.20577914631109,
  "tail_speed_mean_m_s": 0.2325528151996426,
  "tail_speed_rms_m_s": 0.23255281520060306,
  "tail_sensor_speed_mean_m_s": 0.23204974218634436,
  "tail_fk_speed_mean_m_s": 0.23204779197991604,
  "peak_tilt_rad": 0.14048398626657677,
  "peak_wheel_torque_nm": 0.8821277618408203,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 39.79876857303316
}
```
