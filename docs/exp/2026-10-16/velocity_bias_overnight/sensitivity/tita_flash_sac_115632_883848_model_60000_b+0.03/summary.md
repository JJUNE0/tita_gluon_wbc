# tita_flash_sac_115632_883848_model_60000_b+0.03

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_60000_b+0.03",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_60000",
    "duration": 40.0,
    "seed": 270,
    "warmup": 8.0,
    "law": {
      "mode": "constant",
      "bias": 0.03
    }
  },
  "checkpoint_sha256": "6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05",
  "onnx_sha256": "f44f07ed44970e3ff565eae67fd9229adf0be5c02215591c52a691ffcbb71b2a",
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
  "initial_physics_sha256": "490180ebc26fe7e12ee32c42daa5e84b7f4bbbccfcbaf6c05a14c248d084e6b4",
  "complete": true,
  "failure": [],
  "duration_s": 40.0,
  "final_drift_m": 0.24624888688731206,
  "max_drift_m": 0.24624888688731206,
  "radial_IAE_m_s": 5.122832650099719,
  "signed_longitudinal_delta_m": 0.24615860020775476,
  "tail_speed_mean_m_s": 0.0059275522558813395,
  "tail_speed_rms_m_s": 0.005927814489999027,
  "tail_sensor_speed_mean_m_s": 0.00591443680444906,
  "tail_fk_speed_mean_m_s": 0.00591638771612459,
  "peak_tilt_rad": 0.06933936334953117,
  "peak_wheel_torque_nm": 0.13194942474365234,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.03,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 3.1617611789843068
}
```
