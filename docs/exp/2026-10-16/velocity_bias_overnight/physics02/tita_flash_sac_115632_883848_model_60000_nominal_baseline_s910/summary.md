# tita_flash_sac_115632_883848_model_60000_nominal_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_60000_nominal_baseline_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_60000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {},
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
  "initial_physics_sha256": "1252bce4e0207a4aac3c95595d0643b19a94014daa95bb3e2172e4884e2862ed",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.9218877230731405,
  "max_drift_m": 0.9218877230731405,
  "radial_IAE_m_s": 27.39486783175782,
  "signed_longitudinal_delta_m": 0.9211636973635958,
  "tail_speed_mean_m_s": 0.015771548500596866,
  "tail_speed_rms_m_s": 0.015773652394495533,
  "tail_sensor_speed_mean_m_s": 0.015737441178107443,
  "tail_fk_speed_mean_m_s": 0.01573882739510299,
  "peak_tilt_rad": 0.06974151180404209,
  "peak_wheel_torque_nm": 0.1519193947315216,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 10.742101993993856
}
```
