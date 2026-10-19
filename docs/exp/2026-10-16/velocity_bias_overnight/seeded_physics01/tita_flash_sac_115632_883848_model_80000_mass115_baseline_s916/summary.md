# tita_flash_sac_115632_883848_model_80000_mass115_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 80677a4fd403aad22ca310d644998b9b9a686da481d6d95eaf8cc02aa67afadc

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_80000_mass115_baseline_s916",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_80000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "mass": 1.15
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
  },
  "checkpoint_sha256": "80677a4fd403aad22ca310d644998b9b9a686da481d6d95eaf8cc02aa67afadc",
  "onnx_sha256": "c7a83d6c9814cc6aa8357e4b0215d65d880dd6b756de2de920967396e901c93b",
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
  "initial_physics_sha256": "8c32f557fab1a95146e4a4090b7b035d5834a2ad82aced394635c1b8955c19de",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 4.46103698974828,
  "max_drift_m": 4.46103698974828,
  "radial_IAE_m_s": 131.76727224114194,
  "signed_longitudinal_delta_m": 4.4490855947216055,
  "tail_speed_mean_m_s": 0.07601373679903055,
  "tail_speed_rms_m_s": 0.07601391271150869,
  "tail_sensor_speed_mean_m_s": 0.07585051869267531,
  "tail_fk_speed_mean_m_s": 0.07585121934261405,
  "peak_tilt_rad": 0.09033514432072254,
  "peak_wheel_torque_nm": 0.4241243302822113,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 10.349581743008457
}
```
