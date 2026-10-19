# tita_flash_sac_115632_883848_model_60000_mass130_m4_s913_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_60000_mass130_m4_s913_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_60000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 913,
    "estimator": "fk",
    "controller": "m4",
    "physics": {
      "mass": 1.3
    },
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
  "initial_physics_sha256": "f01d75275d2e16bfe7d07d51ad721924a15f67360825dc322e6df0ba697a6b17",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 15.862773374251265,
  "max_drift_m": 19.488743367410624,
  "radial_IAE_m_s": 4383.467298057472,
  "signed_longitudinal_delta_m": -14.550356464085633,
  "tail_speed_mean_m_s": -0.10000720940999476,
  "tail_speed_rms_m_s": 0.10000720987661535,
  "tail_sensor_speed_mean_m_s": -0.09930397408496515,
  "tail_fk_speed_mean_m_s": -0.09952599717598956,
  "peak_tilt_rad": 0.06649880118448559,
  "peak_wheel_torque_nm": 0.2618612051010132,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 72.19957543205237
}
```
