# tita_flash_sac_115632_883848_model_55000_com_plus5mm_v03_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: bb5591e26f71829becb4dab5c4e2effcd37054b9722c650dbf0e2ba993329aa7

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_55000_com_plus5mm_v03_s916",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_55000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "com": 0.005
    },
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
  "checkpoint_sha256": "bb5591e26f71829becb4dab5c4e2effcd37054b9722c650dbf0e2ba993329aa7",
  "onnx_sha256": "8e2044f08b14f84be2b6152fb6085b58a0f6e377394a8fa0f7c69ebac1c08718",
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
  "initial_physics_sha256": "1e57e4ee8ee5650e474b15bffcb0f1fe9c3866d7ac97ed746fdebc5aba0c1ea9",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.01286950326909258,
  "max_drift_m": 0.05590958247421826,
  "radial_IAE_m_s": 0.7677614526672386,
  "signed_longitudinal_delta_m": -0.012852512067395887,
  "tail_speed_mean_m_s": -3.755132192067372e-05,
  "tail_speed_rms_m_s": 3.7844902284265165e-05,
  "tail_sensor_speed_mean_m_s": -3.71364116397248e-05,
  "tail_fk_speed_mean_m_s": -3.429790364620284e-05,
  "peak_tilt_rad": 0.09192194995167768,
  "peak_wheel_torque_nm": 1.0225780010223389,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.2847681344813711,
  "final_integral_m_s": 0.2847681344813711,
  "elapsed_wall_s": 12.640848203969654
}
```
