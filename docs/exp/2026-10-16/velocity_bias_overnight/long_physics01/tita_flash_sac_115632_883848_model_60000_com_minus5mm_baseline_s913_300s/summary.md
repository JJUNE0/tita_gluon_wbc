# tita_flash_sac_115632_883848_model_60000_com_minus5mm_baseline_s913_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_60000_com_minus5mm_baseline_s913_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_60000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 913,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "com": -0.005
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
  "initial_physics_sha256": "fe0ce59e2ecfc91c47bba60dcfeecec831868c751be20b59d55275193d9057cf",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.9106789526164246,
  "max_drift_m": 0.9106789526164246,
  "radial_IAE_m_s": 78.88939115206233,
  "signed_longitudinal_delta_m": 0.866826939986875,
  "tail_speed_mean_m_s": 0.006398397964139173,
  "tail_speed_rms_m_s": 0.006398709833125873,
  "tail_sensor_speed_mean_m_s": 0.006383884296616413,
  "tail_fk_speed_mean_m_s": 0.006385783991026898,
  "peak_tilt_rad": 0.0668201576302061,
  "peak_wheel_torque_nm": 0.14255540072917938,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 39.18811693001771
}
```
