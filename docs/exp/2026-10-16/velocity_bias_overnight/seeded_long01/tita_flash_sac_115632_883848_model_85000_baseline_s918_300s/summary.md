# tita_flash_sac_115632_883848_model_85000_baseline_s918_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d1530cc4acd3186dfa88b59087ef850fd51f024ba7eba3252bc14a6549cc77d7

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_85000_baseline_s918_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_85000",
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
  "checkpoint_sha256": "d1530cc4acd3186dfa88b59087ef850fd51f024ba7eba3252bc14a6549cc77d7",
  "onnx_sha256": "1ed320e4785fe0edd047b9aa7e4185e975602f208fcf3deca0a9aa486c76114c",
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
  "initial_physics_sha256": "e2ae3416dc46d5de0e2ba3bbc52d43fc2f9036bcf7591f0263ad014023bff704",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 38.98848694606926,
  "max_drift_m": 38.98848694606926,
  "radial_IAE_m_s": 5775.4211006407895,
  "signed_longitudinal_delta_m": 38.73594235744918,
  "tail_speed_mean_m_s": 0.13224940036906968,
  "tail_speed_rms_m_s": 0.1322494004238204,
  "tail_sensor_speed_mean_m_s": 0.131962985790179,
  "tail_fk_speed_mean_m_s": 0.13196308650277921,
  "peak_tilt_rad": 0.06759990927529014,
  "peak_wheel_torque_nm": 0.15798133611679077,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 52.19486381002935
}
```
