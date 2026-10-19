# tita_flash_sac_193248_068255_model_75000_kick+0.2_baseline_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 3f7331c3912ccec2acc34ba899d124f69c63f6969c89cf609ed1c0b8f22fcd9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_75000_kick+0.2_baseline_s917",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_75000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 917,
    "estimator": "fk",
    "guarded": false,
    "kick": 0.2,
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
  },
  "checkpoint_sha256": "3f7331c3912ccec2acc34ba899d124f69c63f6969c89cf609ed1c0b8f22fcd9a",
  "onnx_sha256": "ba89df992b5d2cb9fbeaff0a274ee0d50d022a90cd2982cdd88750a3adf35d15",
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
  "initial_physics_sha256": "7465ac50b122481f12343d910466b605723f415e9921a374258c219650bb8437",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 12.511545402716715,
  "max_drift_m": 12.511545402716715,
  "radial_IAE_m_s": 354.794789635417,
  "signed_longitudinal_delta_m": -10.925896230512338,
  "tail_speed_mean_m_s": -0.2540495741512168,
  "tail_speed_rms_m_s": 0.25413758710597495,
  "tail_sensor_speed_mean_m_s": -0.25375429754039514,
  "tail_fk_speed_mean_m_s": -0.25378080844108053,
  "peak_tilt_rad": 0.06832050047212701,
  "peak_wheel_torque_nm": 1.6686437129974365,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 10.602878892037552
}
```
