# tita_flash_sac_115632_883848_model_80000_nominal_v03_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 80677a4fd403aad22ca310d644998b9b9a686da481d6d95eaf8cc02aa67afadc

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_80000_nominal_v03_s916",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_80000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": true,
    "physics": {},
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
  "initial_physics_sha256": "b2bd653bd60f7439a1274bc67a99faa3321975fd56d984e5fdf2f1c0148027ad",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.13018827739391045,
  "max_drift_m": 0.13859381317625577,
  "radial_IAE_m_s": 7.484945251255391,
  "signed_longitudinal_delta_m": 0.13015144846688978,
  "tail_speed_mean_m_s": 0.00013199283170484775,
  "tail_speed_rms_m_s": 0.00013826135450411883,
  "tail_sensor_speed_mean_m_s": 0.000131610047290456,
  "tail_fk_speed_mean_m_s": 0.00013189288247246483,
  "peak_tilt_rad": 0.08429119137271623,
  "peak_wheel_torque_nm": 0.7028135657310486,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.8184528089725404,
  "final_integral_m_s": 0.8184528089725404,
  "elapsed_wall_s": 9.070880074985325
}
```
