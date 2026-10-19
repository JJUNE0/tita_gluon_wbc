# p000_tita_flash_sac_193248_068255_model_95000

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a9ca81d693e2ee34f29bbb8746ae6c7a09f1a201d1d579d15a861fab83818441

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "p000_tita_flash_sac_193248_068255_model_95000",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_95000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "physics": {},
    "kick": -0.2,
    "law": {
      "kp": 0.0,
      "ki": 0.5,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0,
      "seed_gain": 2.0
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
  "final_drift_m": 0.10871283134301847,
  "max_drift_m": 0.4627219448629905,
  "radial_IAE_m_s": 7.468076008682051,
  "signed_longitudinal_delta_m": -0.10863503128535251,
  "tail_speed_mean_m_s": -4.977478939502625e-06,
  "tail_speed_rms_m_s": 3.451351392718809e-05,
  "tail_sensor_speed_mean_m_s": -4.685592684924935e-06,
  "tail_fk_speed_mean_m_s": -5.340878599203174e-06,
  "peak_tilt_rad": 0.08305517964278675,
  "peak_wheel_torque_nm": 1.668466329574585,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.23708525712884468,
  "final_integral_m_s": -0.23708525712884468,
  "elapsed_wall_s": 5.07034091395326
}
```
