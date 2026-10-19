# tita_flash_sac_115632_883848_model_80000_com_plus5mm_v03_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 80677a4fd403aad22ca310d644998b9b9a686da481d6d95eaf8cc02aa67afadc

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_80000_com_plus5mm_v03_s916",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_80000",
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
  "initial_physics_sha256": "990a9f138a920acdb8337effe68b6594e0c3ef303cee6402e4b61a5288ff051e",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.12616395845624745,
  "max_drift_m": 0.14115811426498348,
  "radial_IAE_m_s": 7.2589750739587835,
  "signed_longitudinal_delta_m": 0.12613600937749453,
  "tail_speed_mean_m_s": 0.0001531820689183331,
  "tail_speed_rms_m_s": 0.0001532361980967531,
  "tail_sensor_speed_mean_m_s": 0.00015256007700509256,
  "tail_fk_speed_mean_m_s": 0.00015247179657236167,
  "peak_tilt_rad": 0.08627901704126706,
  "peak_wheel_torque_nm": 0.7652333378791809,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.8652691552259058,
  "final_integral_m_s": 0.8652691552259058,
  "elapsed_wall_s": 10.437470317992847
}
```
