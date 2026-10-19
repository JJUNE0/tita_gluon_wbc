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
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0,
      "gain_velocity": 0.1,
      "gain_tau": 1.0,
      "gain_floor": 0.1,
      "gain_power": 3.0
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
  "final_drift_m": 3.703770970337612,
  "max_drift_m": 3.703770970337612,
  "radial_IAE_m_s": 103.25454398149753,
  "signed_longitudinal_delta_m": 3.613221873651809,
  "tail_speed_mean_m_s": 0.07705124327380064,
  "tail_speed_rms_m_s": 0.41523644000569854,
  "tail_sensor_speed_mean_m_s": 0.07880821329726814,
  "tail_fk_speed_mean_m_s": 0.07697523161188813,
  "peak_tilt_rad": 0.22109472221348359,
  "peak_wheel_torque_nm": 3.3523216247558594,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.6494179173320418,
  "final_integral_m_s": 1.0850291016580236,
  "elapsed_wall_s": 9.24667134496849
}
```
