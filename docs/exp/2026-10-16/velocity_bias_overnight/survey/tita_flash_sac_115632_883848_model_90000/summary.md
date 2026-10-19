# tita_flash_sac_115632_883848_model_90000

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 4930085834f72c133d65563169762514342959361a6d71630216f5f608b0531f

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_90000",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_90000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 270,
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
  "initial_physics_sha256": "b314020b1b325e087ac6242a342b47edad7717481a8f959ea065d4b6007630fd",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 6.7461652189897805,
  "max_drift_m": 6.7461652189897805,
  "radial_IAE_m_s": 201.41287093250355,
  "signed_longitudinal_delta_m": 6.739474721153431,
  "tail_speed_mean_m_s": 0.1136155828600138,
  "tail_speed_rms_m_s": 0.11361577229673811,
  "tail_sensor_speed_mean_m_s": 0.11336972031228015,
  "tail_fk_speed_mean_m_s": 0.11336791398655863,
  "peak_tilt_rad": 0.06945419996718805,
  "peak_wheel_torque_nm": 0.01220095157623291,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 4.3076309519819915
}
```
