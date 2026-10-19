# tita_flash_sac_115632_883848_model_55000_mass130_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: bb5591e26f71829becb4dab5c4e2effcd37054b9722c650dbf0e2ba993329aa7

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_55000_mass130_baseline_s916",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_55000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "mass": 1.3
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
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
  "initial_physics_sha256": "653fd6842656906304970fb1902158f0afbc35d5a9808ccab9b4039a24b3fb01",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 3.4132921024491782,
  "max_drift_m": 3.4132921024491782,
  "radial_IAE_m_s": 102.21425849088561,
  "signed_longitudinal_delta_m": -3.4074440337859797,
  "tail_speed_mean_m_s": -0.05712335132346985,
  "tail_speed_rms_m_s": 0.05712338659928748,
  "tail_sensor_speed_mean_m_s": -0.057000259797628565,
  "tail_fk_speed_mean_m_s": -0.05699923316095248,
  "peak_tilt_rad": 0.10880805984326325,
  "peak_wheel_torque_nm": 0.1906581073999405,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 13.791836218966637
}
```
