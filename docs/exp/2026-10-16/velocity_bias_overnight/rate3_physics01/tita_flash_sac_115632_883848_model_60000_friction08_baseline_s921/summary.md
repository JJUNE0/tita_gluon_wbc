# tita_flash_sac_115632_883848_model_60000_friction08_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_60000_friction08_baseline_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_60000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "friction": 0.8
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
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
  "initial_physics_sha256": "2e7fa473dc55be3ee7a380f9a837d6e3d6677a6e66be324eefe71551ef343a38",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.9158519205821212,
  "max_drift_m": 0.9158519205821212,
  "radial_IAE_m_s": 27.583332351085772,
  "signed_longitudinal_delta_m": 0.9140724690554506,
  "tail_speed_mean_m_s": 0.015187737268127109,
  "tail_speed_rms_m_s": 0.015189229337407295,
  "tail_sensor_speed_mean_m_s": 0.01515517444529532,
  "tail_fk_speed_mean_m_s": 0.015156757194875786,
  "peak_tilt_rad": 0.07082745107801891,
  "peak_wheel_torque_nm": 0.14368480443954468,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 8.54881420196034
}
```
