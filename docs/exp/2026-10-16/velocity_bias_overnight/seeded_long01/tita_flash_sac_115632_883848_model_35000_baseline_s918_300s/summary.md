# tita_flash_sac_115632_883848_model_35000_baseline_s918_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 04d8993b85810ece43a5d202a8a86b46097dcc9e30ce2c7825e73f538f9beab6

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_35000_baseline_s918_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_35000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 918,
    "estimator": "fk",
    "guarded": false,
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
  "initial_physics_sha256": "c01ddcbda68e74b8d4adeb98519d14dbb519993944e6647edac1080d5ab564cf",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 68.16787259056075,
  "max_drift_m": 68.16787259056075,
  "radial_IAE_m_s": 10313.110820782806,
  "signed_longitudinal_delta_m": 65.24985904209639,
  "tail_speed_mean_m_s": 0.23255281635694397,
  "tail_speed_rms_m_s": 0.23255281635796227,
  "tail_sensor_speed_mean_m_s": 0.2320497477222679,
  "tail_fk_speed_mean_m_s": 0.2320477936777726,
  "peak_tilt_rad": 0.1405180041323868,
  "peak_wheel_torque_nm": 0.8839516639709473,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 60.92016929498641
}
```
