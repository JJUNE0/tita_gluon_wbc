# tita_flash_sac_115632_883848_model_60000_v02_s911_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_60000_v02_s911_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_60000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 911,
    "estimator": "fk",
    "runtime": true,
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
  "initial_physics_sha256": "4fa09250b2e3cc4fc8399d53bc785f070ef3b1f1301eab90b6d72b77744cbeed",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.004482912473324219,
  "max_drift_m": 0.007034642519429578,
  "radial_IAE_m_s": 1.3688335428075242,
  "signed_longitudinal_delta_m": 0.0043806847152988385,
  "tail_speed_mean_m_s": -7.516208844679556e-07,
  "tail_speed_rms_m_s": 7.725120304285204e-07,
  "tail_sensor_speed_mean_m_s": -1.5801390946272356e-06,
  "tail_fk_speed_mean_m_s": 5.776272474024165e-07,
  "peak_tilt_rad": 0.06929000586499012,
  "peak_wheel_torque_nm": 0.2009192407131195,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.05272235149227877,
  "final_integral_m_s": 0.052720911828986396,
  "elapsed_wall_s": 63.86988797201775
}
```
