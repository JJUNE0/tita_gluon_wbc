# tita_flash_sac_115632_883848_model_60000_v03_s918_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_60000_v03_s918_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_60000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 918,
    "estimator": "fk",
    "guarded": true,
    "law": {
      "kp": 0.0,
      "ki": 4.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0,
      "seed_gain": 3.0
    },
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
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
  "initial_physics_sha256": "eb56f0041445c657351c1c0fd66d0dab00823a96a3d588a19c1708de1d21159d",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.003515234792608688,
  "max_drift_m": 0.007974819719174017,
  "radial_IAE_m_s": 0.9710207924916097,
  "signed_longitudinal_delta_m": 0.0033395797556890804,
  "tail_speed_mean_m_s": 1.4152914909414356e-07,
  "tail_speed_rms_m_s": 4.900017123148676e-07,
  "tail_sensor_speed_mean_m_s": -6.696571301997845e-07,
  "tail_fk_speed_mean_m_s": 1.482357687040557e-06,
  "peak_tilt_rad": 0.06939398669000796,
  "peak_wheel_torque_nm": 0.19128477573394775,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.052706478204080406,
  "final_integral_m_s": 0.052706478204080406,
  "elapsed_wall_s": 43.95542314503109
}
```
