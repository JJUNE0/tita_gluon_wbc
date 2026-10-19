# p004_tita_flash_sac_115632_883848_model_60000

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "p004_tita_flash_sac_115632_883848_model_60000",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_60000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 270,
    "law": {
      "kp": -2.0,
      "ki": 5.0,
      "tau": 0.1,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 1.0,
      "ramp": 1.5
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
  "final_drift_m": 0.009070802727168384,
  "max_drift_m": 0.019433333741211787,
  "radial_IAE_m_s": 0.5674011797071311,
  "signed_longitudinal_delta_m": 0.009063284247714274,
  "tail_speed_mean_m_s": -1.6658676770829965e-05,
  "tail_speed_rms_m_s": 2.008866409881032e-05,
  "tail_sensor_speed_mean_m_s": -1.6667836469778806e-05,
  "tail_fk_speed_mean_m_s": -1.4529257685365697e-05,
  "peak_tilt_rad": 0.06938740117347875,
  "peak_wheel_torque_nm": 0.16251957416534424,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.04702463273076918,
  "final_integral_m_s": 0.04700667974505096,
  "elapsed_wall_s": 4.627382261969615
}
```
