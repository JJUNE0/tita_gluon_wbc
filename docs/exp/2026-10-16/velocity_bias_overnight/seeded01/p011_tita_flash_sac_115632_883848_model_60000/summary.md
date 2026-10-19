# p011_tita_flash_sac_115632_883848_model_60000

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "p011_tita_flash_sac_115632_883848_model_60000",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_60000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "physics": {},
    "kick": 0.0,
    "law": {
      "kp": 0.0,
      "ki": 2.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0,
      "seed_gain": 5.0
    }
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
  "initial_physics_sha256": "1252bce4e0207a4aac3c95595d0643b19a94014daa95bb3e2172e4884e2862ed",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.006394252145026363,
  "max_drift_m": 0.007310418601654607,
  "radial_IAE_m_s": 0.3491652812792101,
  "signed_longitudinal_delta_m": -0.00638682198923548,
  "tail_speed_mean_m_s": -4.807596034083609e-05,
  "tail_speed_rms_m_s": 4.8941842405574406e-05,
  "tail_sensor_speed_mean_m_s": -4.8066829016715766e-05,
  "tail_fk_speed_mean_m_s": -4.592694765129413e-05,
  "peak_tilt_rad": 0.06924175608200489,
  "peak_wheel_torque_nm": 0.22683997452259064,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.047432291767241945,
  "final_integral_m_s": 0.047432291767241945,
  "elapsed_wall_s": 4.522086769051384
}
```
