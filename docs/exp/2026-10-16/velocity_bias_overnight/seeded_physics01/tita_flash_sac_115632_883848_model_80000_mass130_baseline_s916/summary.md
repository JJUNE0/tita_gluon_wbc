# tita_flash_sac_115632_883848_model_80000_mass130_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 80677a4fd403aad22ca310d644998b9b9a686da481d6d95eaf8cc02aa67afadc

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_80000_mass130_baseline_s916",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_80000",
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
  "initial_physics_sha256": "a45aa2725de91c3d02f2c19cecb465832129998917cf15313099d5e6b2080caa",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 1.9782095956814778,
  "max_drift_m": 1.9782095956814778,
  "radial_IAE_m_s": 60.82460932429237,
  "signed_longitudinal_delta_m": -1.974278227608273,
  "tail_speed_mean_m_s": -0.0316958995456737,
  "tail_speed_rms_m_s": 0.03169615140930377,
  "tail_sensor_speed_mean_m_s": -0.03162721713284134,
  "tail_fk_speed_mean_m_s": -0.03162754045599874,
  "peak_tilt_rad": 0.08227007005641673,
  "peak_wheel_torque_nm": 0.3032150864601135,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 10.72420678997878
}
```
