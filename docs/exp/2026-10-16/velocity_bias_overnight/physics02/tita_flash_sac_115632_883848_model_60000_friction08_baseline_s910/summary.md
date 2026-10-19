# tita_flash_sac_115632_883848_model_60000_friction08_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_60000_friction08_baseline_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_60000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
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
  "initial_physics_sha256": "4cfcca0685b5cec90e026911fe8500beee893ba5594f5a671cfc80b7ccdb33b6",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.9156274466892945,
  "max_drift_m": 0.9156274466892945,
  "radial_IAE_m_s": 27.553763138229264,
  "signed_longitudinal_delta_m": 0.9139037503164629,
  "tail_speed_mean_m_s": 0.015212125777750864,
  "tail_speed_rms_m_s": 0.015213810765813704,
  "tail_sensor_speed_mean_m_s": 0.015179458546010022,
  "tail_fk_speed_mean_m_s": 0.015180988441877446,
  "peak_tilt_rad": 0.07076969319377513,
  "peak_wheel_torque_nm": 0.14399755001068115,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 10.928597010031808
}
```
