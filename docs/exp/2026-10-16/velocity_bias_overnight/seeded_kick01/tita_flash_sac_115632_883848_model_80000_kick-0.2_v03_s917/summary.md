# tita_flash_sac_115632_883848_model_80000_kick-0.2_v03_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 80677a4fd403aad22ca310d644998b9b9a686da481d6d95eaf8cc02aa67afadc

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_80000_kick-0.2_v03_s917",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_80000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 917,
    "estimator": "fk",
    "guarded": true,
    "kick": -0.2,
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
  "initial_physics_sha256": "4522534b01716c994e200c377aeb82600d03c8b7a56d10b8305d244bad3a7683",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.122616904367049,
  "max_drift_m": 0.12590418160176,
  "radial_IAE_m_s": 6.89538563635551,
  "signed_longitudinal_delta_m": 0.1225503752715281,
  "tail_speed_mean_m_s": 0.00013241816572452528,
  "tail_speed_rms_m_s": 0.00013872037504436048,
  "tail_sensor_speed_mean_m_s": 0.000132038903896242,
  "tail_fk_speed_mean_m_s": 0.0001323172672830529,
  "peak_tilt_rad": 0.0842911779423483,
  "peak_wheel_torque_nm": 1.6633186340332031,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.8183237269019925,
  "final_integral_m_s": 0.8183237269019925,
  "elapsed_wall_s": 12.061777141992934
}
```
