# tita_flash_sac_193248_068255_model_75000_kick-0.2_v03_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 3f7331c3912ccec2acc34ba899d124f69c63f6969c89cf609ed1c0b8f22fcd9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_75000_kick-0.2_v03_s917",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_75000",
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
  "initial_physics_sha256": "c7abb82a5a457b325adb86c54c1cdf6c12f057091ca9891022d7fc94c402b64f",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.006584671985160746,
  "max_drift_m": 0.1602933333891112,
  "radial_IAE_m_s": 0.9020222359723615,
  "signed_longitudinal_delta_m": -0.006584606158519544,
  "tail_speed_mean_m_s": 2.9621149883804427e-05,
  "tail_speed_rms_m_s": 2.9643197827265444e-05,
  "tail_sensor_speed_mean_m_s": 2.9719830654522713e-05,
  "tail_fk_speed_mean_m_s": 2.928619001389248e-05,
  "peak_tilt_rad": 0.12540358917777117,
  "peak_wheel_torque_nm": 1.7469968795776367,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.27871409057838953,
  "final_integral_m_s": -0.27871409057838953,
  "elapsed_wall_s": 13.363251582952216
}
```
