# p001_tita_flash_sac_193248_068255_model_95000_runtime

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a9ca81d693e2ee34f29bbb8746ae6c7a09f1a201d1d579d15a861fab83818441

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "p001_tita_flash_sac_193248_068255_model_95000_runtime",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_95000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "physics": {},
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
    "runtime": true,
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0",
    "controller_source_sha256": "6056e5bd50e0d84e7e554e390f2ede0726c82adf059af80911969c1286a3cded"
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
  "final_drift_m": 0.012379576773068751,
  "max_drift_m": 0.20826124324136985,
  "radial_IAE_m_s": 1.64171252647916,
  "signed_longitudinal_delta_m": 0.012267056118089887,
  "tail_speed_mean_m_s": -3.0595597265487144e-06,
  "tail_speed_rms_m_s": 4.869626170273359e-05,
  "tail_sensor_speed_mean_m_s": -3.2655624170966715e-06,
  "tail_fk_speed_mean_m_s": -3.451035926551995e-06,
  "peak_tilt_rad": 0.13083990445251126,
  "peak_wheel_torque_nm": 1.752636432647705,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.22474434103132604,
  "final_integral_m_s": -0.22474434103132604,
  "elapsed_wall_s": 15.202917296031956
}
```
