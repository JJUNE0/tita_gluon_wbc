# tita_flash_sac_115632_883848_model_60000_kick+0.2_v01

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_60000_kick+0.2_v01",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_60000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 272,
    "physics": {},
    "kick": 0.2,
    "law": {
      "kp": 2.0,
      "ki": 10.0,
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
  "initial_physics_sha256": "b6909a7d5e216ef355e302c4b3b78ff24b822631a9c8913fcf8b67e705174b64",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.005656580298111213,
  "max_drift_m": 0.07298261445832294,
  "radial_IAE_m_s": 0.4102670557297282,
  "signed_longitudinal_delta_m": 0.0056560991766129495,
  "tail_speed_mean_m_s": -8.565781393382844e-06,
  "tail_speed_rms_m_s": 8.84869144117985e-06,
  "tail_sensor_speed_mean_m_s": -8.50137398363612e-06,
  "tail_fk_speed_mean_m_s": -6.444471462824016e-06,
  "peak_tilt_rad": 0.0952456683317986,
  "peak_wheel_torque_nm": 2.314549207687378,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.046926523320638576,
  "final_integral_m_s": 0.046936098260817634,
  "elapsed_wall_s": 5.019696713949088
}
```
