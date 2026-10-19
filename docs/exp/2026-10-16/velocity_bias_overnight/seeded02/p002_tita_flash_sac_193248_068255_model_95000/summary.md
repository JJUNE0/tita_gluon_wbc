# p002_tita_flash_sac_193248_068255_model_95000

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a9ca81d693e2ee34f29bbb8746ae6c7a09f1a201d1d579d15a861fab83818441

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "p002_tita_flash_sac_193248_068255_model_95000",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_95000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "physics": {},
    "kick": -0.2,
    "law": {
      "kp": 0.0,
      "ki": 3.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0,
      "seed_gain": 3.5
    }
  },
  "checkpoint_sha256": "a9ca81d693e2ee34f29bbb8746ae6c7a09f1a201d1d579d15a861fab83818441",
  "onnx_sha256": "7e9315ab3ff8de6c69ba7599d9f20f2c432877c181d5c6228d4b55646de7b449",
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
  "initial_physics_sha256": "c6d93f6c020f87ac57183534db7ce14b7b116284143d13c8f02b0bd5d02c5605",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.027846020493632186,
  "max_drift_m": 0.23640705953224575,
  "radial_IAE_m_s": 2.528429747294785,
  "signed_longitudinal_delta_m": 0.02777143767802495,
  "tail_speed_mean_m_s": -5.31299547831271e-07,
  "tail_speed_rms_m_s": 3.6113440464238194e-05,
  "tail_sensor_speed_mean_m_s": -5.895789673564313e-07,
  "tail_fk_speed_mean_m_s": -9.221647747105916e-07,
  "peak_tilt_rad": 0.11747037650816772,
  "peak_wheel_torque_nm": 1.7620172500610352,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.23639460546533603,
  "final_integral_m_s": -0.23639460546533603,
  "elapsed_wall_s": 5.200923117983621
}
```
