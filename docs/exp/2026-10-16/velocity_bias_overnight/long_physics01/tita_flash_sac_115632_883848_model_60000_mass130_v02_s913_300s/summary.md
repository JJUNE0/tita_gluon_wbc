# tita_flash_sac_115632_883848_model_60000_mass130_v02_s913_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_60000_mass130_v02_s913_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_60000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 913,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "mass": 1.3
    },
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
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
  "initial_physics_sha256": "f01d75275d2e16bfe7d07d51ad721924a15f67360825dc322e6df0ba697a6b17",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.034633920000825526,
  "max_drift_m": 0.06412284120016999,
  "radial_IAE_m_s": 11.096902506050633,
  "signed_longitudinal_delta_m": -0.03424466966961009,
  "tail_speed_mean_m_s": 1.1835791035832512e-05,
  "tail_speed_rms_m_s": 0.016118708576706536,
  "tail_sensor_speed_mean_m_s": -0.001640265848864748,
  "tail_fk_speed_mean_m_s": -6.0835078005565985e-05,
  "peak_tilt_rad": 0.17471145655573905,
  "peak_wheel_torque_nm": 5.478498935699463,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.4120332312011838,
  "final_integral_m_s": -0.4186439538151912,
  "elapsed_wall_s": 62.71956016798504
}
```
