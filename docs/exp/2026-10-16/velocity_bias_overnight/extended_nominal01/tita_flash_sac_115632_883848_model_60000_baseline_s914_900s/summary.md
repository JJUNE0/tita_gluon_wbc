# tita_flash_sac_115632_883848_model_60000_baseline_s914_900s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_60000_baseline_s914_900s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_60000",
    "duration": 900.0,
    "warmup": 1.2,
    "seed": 914,
    "estimator": "fk",
    "runtime": false,
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05",
  "onnx_sha256": "f44f07ed44970e3ff565eae67fd9229adf0be5c02215591c52a691ffcbb71b2a",
  "input_columns": [
    "velocity_bias_m_s",
    "filtered_velocity_m_s",
    "integral_m_s"
  ],
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
  "initial_physics_sha256": "1ff916b458aff131929055d6e4a56ccf621e06306bd67b1df2ef032e8abb86c3",
  "complete": true,
  "failure": [],
  "duration_s": 900.0,
  "final_drift_m": 16.135786209431608,
  "max_drift_m": 16.135786209431608,
  "radial_IAE_m_s": 7356.410944859369,
  "signed_longitudinal_delta_m": 13.33716851880103,
  "tail_speed_mean_m_s": 0.02046575306927169,
  "tail_speed_rms_m_s": 0.020465753388905116,
  "tail_sensor_speed_mean_m_s": 0.0204320869181446,
  "tail_fk_speed_mean_m_s": 0.020435197582432243,
  "peak_tilt_rad": 0.0697414770804019,
  "peak_wheel_torque_nm": 0.15193098783493042,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 118.08995303499978
}
```
