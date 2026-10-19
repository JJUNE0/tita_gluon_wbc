# tita_flash_sac_115632_883848_model_55000_kick+0.2_v03_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: bb5591e26f71829becb4dab5c4e2effcd37054b9722c650dbf0e2ba993329aa7

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_55000_kick+0.2_v03_s917",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_55000",
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
  "initial_physics_sha256": "35d468ebec28a138bea16aa2dbeb43f98d63bddff3a8a4a03dd4e09557d9f687",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.020842367081105033,
  "max_drift_m": 0.13124459607092617,
  "radial_IAE_m_s": 1.3419836964912588,
  "signed_longitudinal_delta_m": -0.020769970481511045,
  "tail_speed_mean_m_s": -4.144561859555497e-05,
  "tail_speed_rms_m_s": 4.163720334633431e-05,
  "tail_sensor_speed_mean_m_s": -4.0994029953324625e-05,
  "tail_fk_speed_mean_m_s": -3.767294368125596e-05,
  "peak_tilt_rad": 0.11284186036220789,
  "peak_wheel_torque_nm": 2.3092329502105713,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.24037755370675382,
  "final_integral_m_s": 0.24037755370675382,
  "elapsed_wall_s": 13.52286714600632
}
```
