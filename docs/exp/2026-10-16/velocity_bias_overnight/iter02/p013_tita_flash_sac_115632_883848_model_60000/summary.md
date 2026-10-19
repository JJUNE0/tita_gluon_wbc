# p013_tita_flash_sac_115632_883848_model_60000

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "p013_tita_flash_sac_115632_883848_model_60000",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_60000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 270,
    "law": {
      "kp": 2.0,
      "ki": 5.0,
      "tau": 0.05,
      "ramp": 0.75,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
    },
    "estimator": "fk"
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
  "duration_s": 60.0,
  "final_drift_m": 0.009088865859484527,
  "max_drift_m": 0.01126050858437517,
  "radial_IAE_m_s": 0.5636904275148185,
  "signed_longitudinal_delta_m": 0.009080894740431758,
  "tail_speed_mean_m_s": -1.62272736594001e-05,
  "tail_speed_rms_m_s": 1.6887006674033596e-05,
  "tail_sensor_speed_mean_m_s": -1.6164679437160687e-05,
  "tail_fk_speed_mean_m_s": -1.4099425539949302e-05,
  "peak_tilt_rad": 0.06933936334953117,
  "peak_wheel_torque_nm": 0.1629399210214615,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.047036521470370886,
  "final_integral_m_s": 0.04705659562542004,
  "elapsed_wall_s": 4.798504925041925
}
```
