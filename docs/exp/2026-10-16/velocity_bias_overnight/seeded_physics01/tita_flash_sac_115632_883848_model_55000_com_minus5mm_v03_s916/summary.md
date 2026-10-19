# tita_flash_sac_115632_883848_model_55000_com_minus5mm_v03_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: bb5591e26f71829becb4dab5c4e2effcd37054b9722c650dbf0e2ba993329aa7

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_55000_com_minus5mm_v03_s916",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_55000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "com": -0.005
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
  "initial_physics_sha256": "709a9e15b7ea00dfeb1d1e697bfa42ee0dab2b2d7271e97f5b021f49e218c1d7",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.004196373107637786,
  "max_drift_m": 0.03658865623092805,
  "radial_IAE_m_s": 0.232409482177242,
  "signed_longitudinal_delta_m": -0.004150422993223788,
  "tail_speed_mean_m_s": -4.130642620905571e-05,
  "tail_speed_rms_m_s": 4.1381775232972125e-05,
  "tail_sensor_speed_mean_m_s": -3.748188332710824e-05,
  "tail_fk_speed_mean_m_s": -3.366981875015819e-05,
  "peak_tilt_rad": 0.08599291560922473,
  "peak_wheel_torque_nm": 0.7479978799819946,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.19665047821570963,
  "final_integral_m_s": 0.19665047821570963,
  "elapsed_wall_s": 13.358424811041914
}
```
