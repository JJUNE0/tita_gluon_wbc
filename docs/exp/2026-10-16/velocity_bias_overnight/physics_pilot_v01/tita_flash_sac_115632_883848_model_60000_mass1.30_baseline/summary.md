# tita_flash_sac_115632_883848_model_60000_mass1.30_baseline

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_60000_mass1.30_baseline",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_60000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 272,
    "physics": {
      "mass": 1.3
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
  "initial_physics_sha256": "d393bd92f9cdf47131e0ad8f9193a9875947ef831a33d735176e1feca2e48122",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 9.371627650770531,
  "max_drift_m": 9.371627650770531,
  "radial_IAE_m_s": 284.71381616905813,
  "signed_longitudinal_delta_m": -9.320289835374787,
  "tail_speed_mean_m_s": -0.1524713819437154,
  "tail_speed_rms_m_s": 0.15248936103021926,
  "tail_sensor_speed_mean_m_s": -0.15214467609539958,
  "tail_fk_speed_mean_m_s": -0.15214188920544708,
  "peak_tilt_rad": 0.058160537841753124,
  "peak_wheel_torque_nm": 0.060046374797821045,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 5.474638280051295
}
```
