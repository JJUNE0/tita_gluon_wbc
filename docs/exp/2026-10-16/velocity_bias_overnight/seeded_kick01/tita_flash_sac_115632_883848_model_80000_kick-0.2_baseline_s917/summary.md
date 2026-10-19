# tita_flash_sac_115632_883848_model_80000_kick-0.2_baseline_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 80677a4fd403aad22ca310d644998b9b9a686da481d6d95eaf8cc02aa67afadc

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_80000_kick-0.2_baseline_s917",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_80000",
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
  "initial_physics_sha256": "4522534b01716c994e200c377aeb82600d03c8b7a56d10b8305d244bad3a7683",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 11.499949381342253,
  "max_drift_m": 11.499949381342253,
  "radial_IAE_m_s": 333.8507668819773,
  "signed_longitudinal_delta_m": 11.453441234145416,
  "tail_speed_mean_m_s": 0.19948597458630393,
  "tail_speed_rms_m_s": 0.19948629265863477,
  "tail_sensor_speed_mean_m_s": 0.1990550832944037,
  "tail_fk_speed_mean_m_s": 0.1990540963103635,
  "peak_tilt_rad": 0.08721803337640655,
  "peak_wheel_torque_nm": 1.9934446811676025,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.813363744004164
}
```
