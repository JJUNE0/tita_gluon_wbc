# p030_tita_flash_sac_115632_883848_model_60000

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "p030_tita_flash_sac_115632_883848_model_60000",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_60000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 270,
    "law": {
      "kp": 5.0,
      "ki": 10.0,
      "tau": 0.2,
      "ramp": 0.25,
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
  "final_drift_m": 0.004382054964396528,
  "max_drift_m": 0.006105426473508866,
  "radial_IAE_m_s": 0.27427109573534225,
  "signed_longitudinal_delta_m": 0.004364452053516368,
  "tail_speed_mean_m_s": -9.097329678236426e-06,
  "tail_speed_rms_m_s": 9.392523042163062e-06,
  "tail_sensor_speed_mean_m_s": -9.05245928497461e-06,
  "tail_fk_speed_mean_m_s": -6.985226250460144e-06,
  "peak_tilt_rad": 0.06933936334953117,
  "peak_wheel_torque_nm": 0.2505743205547333,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.04702405921055504,
  "final_integral_m_s": 0.04704942327014933,
  "elapsed_wall_s": 4.698020351992454
}
```
