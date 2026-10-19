# tita_flash_sac_115632_883848_model_60000_friction08_baseline_s913_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_60000_friction08_baseline_s913_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_60000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 913,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "friction": 0.8
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
  "initial_physics_sha256": "9064ed9941d862540cf642fcf2dbf29af5780286ee8c63e78bd4563550e065da",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 5.277049022335347,
  "max_drift_m": 5.277049022335347,
  "radial_IAE_m_s": 754.8074237001018,
  "signed_longitudinal_delta_m": 5.175594482597452,
  "tail_speed_mean_m_s": 0.019410195053138884,
  "tail_speed_rms_m_s": 0.0194102106795872,
  "tail_sensor_speed_mean_m_s": 0.019368380855746884,
  "tail_fk_speed_mean_m_s": 0.01936980564801419,
  "peak_tilt_rad": 0.07082747211538964,
  "peak_wheel_torque_nm": 0.14368173480033875,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 39.90982307103695
}
```
