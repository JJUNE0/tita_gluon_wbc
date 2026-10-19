# tita_flash_sac_115632_883848_model_10000_kick+0.2_v03_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 48a0379d0b30385cff5ccfe473d0ee136f303e640a505719a82bad5a3e3178a5

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_10000_kick+0.2_v03_s917",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_10000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 917,
    "estimator": "fk",
    "guarded": true,
    "kick": 0.2,
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
  "checkpoint_sha256": "48a0379d0b30385cff5ccfe473d0ee136f303e640a505719a82bad5a3e3178a5",
  "onnx_sha256": "06e48800bb84c9f9275464d939d3614105bfbc1bbe6af1e92522c94faa5f1e15",
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
  "initial_physics_sha256": "f2c7e684704831207e4ff4730a490193e7ee905008716ae3e17b9941ccaf60fd",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.29963072604809643,
  "max_drift_m": 0.3152392973590107,
  "radial_IAE_m_s": 17.615558969562883,
  "signed_longitudinal_delta_m": 0.29962767951194536,
  "tail_speed_mean_m_s": -0.00032194518717291407,
  "tail_speed_rms_m_s": 0.017225228710827527,
  "tail_sensor_speed_mean_m_s": 0.0013891796963884317,
  "tail_fk_speed_mean_m_s": -0.0003912559126153737,
  "peak_tilt_rad": 0.15906798256742838,
  "peak_wheel_torque_nm": 5.451372146606445,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.3379102371260642,
  "final_integral_m_s": 0.3379102371260642,
  "elapsed_wall_s": 9.489671837014612
}
```
