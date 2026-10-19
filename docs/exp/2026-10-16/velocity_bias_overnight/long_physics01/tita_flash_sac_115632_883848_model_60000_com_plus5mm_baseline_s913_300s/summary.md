# tita_flash_sac_115632_883848_model_60000_com_plus5mm_baseline_s913_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_60000_com_plus5mm_baseline_s913_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_60000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 913,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "com": 0.005
    },
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
  "initial_physics_sha256": "18a2833a0f14a3f6032c3a8c88dcf457d5509a0d7546d485fe29095f12b3c5c7",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 9.969745752733276,
  "max_drift_m": 9.969745752733276,
  "radial_IAE_m_s": 1495.4960182516763,
  "signed_longitudinal_delta_m": 9.903720561333156,
  "tail_speed_mean_m_s": 0.03348828055603785,
  "tail_speed_rms_m_s": 0.03348828511583402,
  "tail_sensor_speed_mean_m_s": 0.033415787013787744,
  "tail_fk_speed_mean_m_s": 0.033416606485354966,
  "peak_tilt_rad": 0.07314754286568714,
  "peak_wheel_torque_nm": 0.16778866946697235,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 51.84851281502051
}
```
