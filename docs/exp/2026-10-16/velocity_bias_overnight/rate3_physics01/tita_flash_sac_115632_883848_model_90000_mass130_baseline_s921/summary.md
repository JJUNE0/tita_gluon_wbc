# tita_flash_sac_115632_883848_model_90000_mass130_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 4930085834f72c133d65563169762514342959361a6d71630216f5f608b0531f

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_90000_mass130_baseline_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_90000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "mass": 1.3
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
  },
  "checkpoint_sha256": "4930085834f72c133d65563169762514342959361a6d71630216f5f608b0531f",
  "onnx_sha256": "1d6ffa5d91a15cf74e2abf755c367c1fb151f6e3c740618a6e1fb2fbf28f9379",
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
  "initial_physics_sha256": "e232874bcaf67ddae8106a8d7583f382456a8d0bf7db8d0ea7cbe6dc8fb2d099",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 6.860030504714961,
  "max_drift_m": 6.860030504714961,
  "radial_IAE_m_s": 205.70241353234303,
  "signed_longitudinal_delta_m": -6.857573169788776,
  "tail_speed_mean_m_s": -0.11439651210681263,
  "tail_speed_rms_m_s": 0.11439651393505983,
  "tail_sensor_speed_mean_m_s": -0.11415088428759304,
  "tail_fk_speed_mean_m_s": -0.1141507339085439,
  "peak_tilt_rad": 0.07611503696255362,
  "peak_wheel_torque_nm": 0.764904260635376,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 15.252956791955512
}
```
