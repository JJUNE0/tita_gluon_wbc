# tita_flash_sac_115632_883848_model_60000_com-0.005_baseline

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_60000_com-0.005_baseline",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_60000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 272,
    "physics": {
      "com": -0.005
    },
    "kick": 0.0,
    "law": {
      "mode": "constant",
      "bias": 0.0
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
  "initial_physics_sha256": "6e852968a0a45508ece30abc12e1254f266760f5b7fa9c9871bc3a2c572e626f",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.02114353009069167,
  "max_drift_m": 0.03131810711584824,
  "radial_IAE_m_s": 1.3669518487515964,
  "signed_longitudinal_delta_m": -0.021131189826441573,
  "tail_speed_mean_m_s": 0.0005114831975551247,
  "tail_speed_rms_m_s": 0.0005782350653237929,
  "tail_sensor_speed_mean_m_s": 0.0005103540420530672,
  "tail_fk_speed_mean_m_s": 0.0005124774427169489,
  "peak_tilt_rad": 0.06641765627237817,
  "peak_wheel_torque_nm": 0.11942582577466965,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 5.482090545992833
}
```
