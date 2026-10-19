# p020_tita_flash_sac_115632_883848_model_60000

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "p020_tita_flash_sac_115632_883848_model_60000",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_60000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 270,
    "law": {
      "kp": 2.0,
      "ki": 20.0,
      "tau": 0.05,
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
  "final_drift_m": 0.0020446657058603504,
  "max_drift_m": 0.005229115184253437,
  "radial_IAE_m_s": 0.1303634673532954,
  "signed_longitudinal_delta_m": 0.002005724648599906,
  "tail_speed_mean_m_s": -5.550723801642109e-06,
  "tail_speed_rms_m_s": 5.678002929155486e-06,
  "tail_sensor_speed_mean_m_s": -5.515189251764993e-06,
  "tail_fk_speed_mean_m_s": -3.4469282177422416e-06,
  "peak_tilt_rad": 0.06933936334953117,
  "peak_wheel_torque_nm": 0.2862517833709717,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.04701809641013913,
  "final_integral_m_s": 0.047023118545813244,
  "elapsed_wall_s": 4.700939054018818
}
```
