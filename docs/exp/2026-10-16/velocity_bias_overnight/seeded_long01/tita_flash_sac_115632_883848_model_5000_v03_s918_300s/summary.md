# tita_flash_sac_115632_883848_model_5000_v03_s918_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: cc685c5efb437641f8ad47131a1b737aa37ee01ecbc81e3d5e5a21ebc1ddd90d

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_5000_v03_s918_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_5000",
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
  "checkpoint_sha256": "cc685c5efb437641f8ad47131a1b737aa37ee01ecbc81e3d5e5a21ebc1ddd90d",
  "onnx_sha256": "4d80b373930fd59198e3fc588870f929175201ad8b748405f7e94231464a4d30",
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
  "initial_physics_sha256": "65218c0f51ba1e8e455ead804618fb3569f6936691847505c6cd07e05f04b918",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.018107100171050917,
  "max_drift_m": 0.09730478017653044,
  "radial_IAE_m_s": 4.217395154983503,
  "signed_longitudinal_delta_m": 0.018021614231926105,
  "tail_speed_mean_m_s": 5.916151523424605e-06,
  "tail_speed_rms_m_s": 0.0005441827232006116,
  "tail_sensor_speed_mean_m_s": 9.031763900839361e-05,
  "tail_fk_speed_mean_m_s": 1.0562415213518132e-05,
  "peak_tilt_rad": 0.1968112576942027,
  "peak_wheel_torque_nm": 3.3306238651275635,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.40787149390043825,
  "final_integral_m_s": -0.40787149390043825,
  "elapsed_wall_s": 44.68398985802196
}
```
