# tita_flash_sac_115632_883848_model_55000_kick-0.2_baseline_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: bb5591e26f71829becb4dab5c4e2effcd37054b9722c650dbf0e2ba993329aa7

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_55000_kick-0.2_baseline_s917",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_55000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 917,
    "estimator": "fk",
    "guarded": false,
    "kick": -0.2,
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
  "initial_physics_sha256": "ab8579e487c87164d49fa427bdfde0e66d5068deaa079f9539c3d830add8e607",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 6.56551626828659,
  "max_drift_m": 6.56551626828659,
  "radial_IAE_m_s": 191.5426196235797,
  "signed_longitudinal_delta_m": 6.457772195229915,
  "tail_speed_mean_m_s": 0.11306606903790399,
  "tail_speed_rms_m_s": 0.11306608171979154,
  "tail_sensor_speed_mean_m_s": 0.11282206804355224,
  "tail_fk_speed_mean_m_s": 0.11282357565106552,
  "peak_tilt_rad": 0.0909034331818126,
  "peak_wheel_torque_nm": 1.7707115411758423,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 11.621554023004137
}
```
