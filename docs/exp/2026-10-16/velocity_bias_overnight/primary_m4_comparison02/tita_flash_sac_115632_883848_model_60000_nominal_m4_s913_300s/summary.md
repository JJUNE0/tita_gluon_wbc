# tita_flash_sac_115632_883848_model_60000_nominal_m4_s913_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_60000_nominal_m4_s913_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_60000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 913,
    "estimator": "fk",
    "controller": "m4",
    "physics": {},
    "law": {
      "mode": "m4"
    }
  },
  "checkpoint_sha256": "6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05",
  "onnx_sha256": "f44f07ed44970e3ff565eae67fd9229adf0be5c02215591c52a691ffcbb71b2a",
  "input_columns": [
    "total_residual_nm",
    "lqr_correction_nm",
    "fixed_bias_nm"
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
  "initial_physics_sha256": "767b3e7f7847a8e838f15e263b866e6ed7630cea5577e18891611065effc766c",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.19990159951296838,
  "max_drift_m": 0.19990159951296838,
  "radial_IAE_m_s": 17.504223350568143,
  "signed_longitudinal_delta_m": 0.18991006890383788,
  "tail_speed_mean_m_s": 0.0013459239255143862,
  "tail_speed_rms_m_s": 0.0013460964355635715,
  "tail_sensor_speed_mean_m_s": 0.0013422185243199712,
  "tail_fk_speed_mean_m_s": 0.0013442975148184268,
  "peak_tilt_rad": 0.06939400622474179,
  "peak_wheel_torque_nm": 0.17864422500133514,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 63.62656723300461
}
```
