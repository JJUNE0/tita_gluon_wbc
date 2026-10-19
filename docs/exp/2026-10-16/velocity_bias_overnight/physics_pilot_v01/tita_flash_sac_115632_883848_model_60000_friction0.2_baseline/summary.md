# tita_flash_sac_115632_883848_model_60000_friction0.2_baseline

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_60000_friction0.2_baseline",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_60000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 272,
    "physics": {
      "friction": 0.2
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
  "initial_physics_sha256": "c9f5d063c438c02e357d98dbe7ca8149d3a49a72d7f29049640456bf4d57a642",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.9441615262270445,
  "max_drift_m": 0.9441615262270445,
  "radial_IAE_m_s": 29.5456176788968,
  "signed_longitudinal_delta_m": 0.7210080013067994,
  "tail_speed_mean_m_s": 0.01710640343083227,
  "tail_speed_rms_m_s": 0.017106403639727232,
  "tail_sensor_speed_mean_m_s": 0.01705518459758285,
  "tail_fk_speed_mean_m_s": 0.01708693847124197,
  "peak_tilt_rad": 0.06124169045932559,
  "peak_wheel_torque_nm": 0.07231806218624115,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 5.52856566401897
}
```
