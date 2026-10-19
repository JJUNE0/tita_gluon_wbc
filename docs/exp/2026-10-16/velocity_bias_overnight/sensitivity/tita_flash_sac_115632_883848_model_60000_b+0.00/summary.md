# tita_flash_sac_115632_883848_model_60000_b+0.00

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_60000_b+0.00",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_60000",
    "duration": 40.0,
    "seed": 270,
    "warmup": 8.0,
    "law": {
      "mode": "constant",
      "bias": 0.0
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
  "final_drift_m": 0.6089863365769003,
  "max_drift_m": 0.6089863365769003,
  "radial_IAE_m_s": 12.178752926480806,
  "signed_longitudinal_delta_m": 0.6087968584283363,
  "tail_speed_mean_m_s": 0.015182994586185132,
  "tail_speed_rms_m_s": 0.01518418211222356,
  "tail_sensor_speed_mean_m_s": 0.015149652629809928,
  "tail_fk_speed_mean_m_s": 0.015151355472869403,
  "peak_tilt_rad": 0.06933936334953117,
  "peak_wheel_torque_nm": 0.12339599430561066,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 3.280763894028496
}
```
