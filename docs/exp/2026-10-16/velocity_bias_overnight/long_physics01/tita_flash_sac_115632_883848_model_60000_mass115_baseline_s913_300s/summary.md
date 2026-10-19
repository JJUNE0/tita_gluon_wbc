# tita_flash_sac_115632_883848_model_60000_mass115_baseline_s913_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_60000_mass115_baseline_s913_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_60000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 913,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "mass": 1.15
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
  "initial_physics_sha256": "de102d7b611657224b65a0cfa5b6c6a8b03b2ba0da773d30b4afd17f4b348517",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 26.103070345859898,
  "max_drift_m": 26.103070345859898,
  "radial_IAE_m_s": 3962.4006255308745,
  "signed_longitudinal_delta_m": -24.280695448087886,
  "tail_speed_mean_m_s": -0.08888004846204933,
  "tail_speed_rms_m_s": 0.08888012201486695,
  "tail_sensor_speed_mean_m_s": -0.08868971590894029,
  "tail_fk_speed_mean_m_s": -0.08868661660745354,
  "peak_tilt_rad": 0.06284956135908715,
  "peak_wheel_torque_nm": 0.14200067520141602,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 51.5299814720056
}
```
