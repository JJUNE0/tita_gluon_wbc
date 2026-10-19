# tita_flash_sac_115632_883848_model_60000_mass115_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_60000_mass115_baseline_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_60000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
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
  "initial_physics_sha256": "708b85f64ac481614c03670a578bec7f0d5b44bb459afcf70b2a1a339c249e4a",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 5.346641940444566,
  "max_drift_m": 5.346641940444566,
  "radial_IAE_m_s": 160.10459546242814,
  "signed_longitudinal_delta_m": -5.328924948305345,
  "tail_speed_mean_m_s": -0.08946523015617346,
  "tail_speed_rms_m_s": 0.08946523161019246,
  "tail_sensor_speed_mean_m_s": -0.08927222920643178,
  "tail_fk_speed_mean_m_s": -0.08926997874840771,
  "peak_tilt_rad": 0.06220130637972465,
  "peak_wheel_torque_nm": 0.14254310727119446,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 12.558579080970958
}
```
