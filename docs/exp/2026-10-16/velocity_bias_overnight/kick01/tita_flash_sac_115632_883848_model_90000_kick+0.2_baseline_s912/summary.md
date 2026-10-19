# tita_flash_sac_115632_883848_model_90000_kick+0.2_baseline_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 4930085834f72c133d65563169762514342959361a6d71630216f5f608b0531f

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_90000_kick+0.2_baseline_s912",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_90000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 912,
    "estimator": "fk",
    "runtime": false,
    "kick": 0.2,
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "4930085834f72c133d65563169762514342959361a6d71630216f5f608b0531f",
  "onnx_sha256": "1d6ffa5d91a15cf74e2abf755c367c1fb151f6e3c740618a6e1fb2fbf28f9379",
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
  "initial_physics_sha256": "517f91e6141871fbd7c74c43d239a2cbf00184c84da7dba3b5341bd71129f4bf",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 6.860410054692121,
  "max_drift_m": 6.860410054692121,
  "radial_IAE_m_s": 208.64762076322432,
  "signed_longitudinal_delta_m": 6.858932484841296,
  "tail_speed_mean_m_s": 0.11340308770831933,
  "tail_speed_rms_m_s": 0.11340332861782067,
  "tail_sensor_speed_mean_m_s": 0.11315764920911121,
  "tail_fk_speed_mean_m_s": 0.11315588931432023,
  "peak_tilt_rad": 0.08517131050566085,
  "peak_wheel_torque_nm": 1.736190915107727,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 14.51895673701074
}
```
