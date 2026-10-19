# tita_flash_sac_115632_883848_model_90000_nominal_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 4930085834f72c133d65563169762514342959361a6d71630216f5f608b0531f

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_90000_nominal_baseline_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_90000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {},
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
  "initial_physics_sha256": "e71e604bf0e1061f3f76c5ca438ebedcba3a488858f7be286770f638e8be9d27",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 6.698160428974797,
  "max_drift_m": 6.698160428974797,
  "radial_IAE_m_s": 199.0938136994511,
  "signed_longitudinal_delta_m": 6.696122511701345,
  "tail_speed_mean_m_s": 0.11337026360857712,
  "tail_speed_rms_m_s": 0.11337051500926575,
  "tail_sensor_speed_mean_m_s": 0.11312487757214723,
  "tail_fk_speed_mean_m_s": 0.11312313713431706,
  "peak_tilt_rad": 0.0704808758078932,
  "peak_wheel_torque_nm": 0.19818493723869324,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 12.639249331958126
}
```
