# tita_flash_sac_115632_883848_model_35000_mass115_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 04d8993b85810ece43a5d202a8a86b46097dcc9e30ce2c7825e73f538f9beab6

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_35000_mass115_baseline_s916",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_35000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "mass": 1.15
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
  "initial_physics_sha256": "4b1275497c63ddd46e9a4983b7372d400f8f95b80224a08aa03fe6d693540f60",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 8.368316391601265,
  "max_drift_m": 8.368316391601265,
  "radial_IAE_m_s": 249.17439463957345,
  "signed_longitudinal_delta_m": 8.36733541272561,
  "tail_speed_mean_m_s": 0.14091743798142295,
  "tail_speed_rms_m_s": 0.14091746789701975,
  "tail_sensor_speed_mean_m_s": 0.1406136018654267,
  "tail_fk_speed_mean_m_s": 0.14061363633257268,
  "peak_tilt_rad": 0.13915447220348898,
  "peak_wheel_torque_nm": 0.7569139003753662,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 15.755814800038934
}
```
