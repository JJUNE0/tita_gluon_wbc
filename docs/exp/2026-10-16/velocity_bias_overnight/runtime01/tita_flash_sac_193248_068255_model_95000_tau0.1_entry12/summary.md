# tita_flash_sac_193248_068255_model_95000_tau0.1_entry12

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a9ca81d693e2ee34f29bbb8746ae6c7a09f1a201d1d579d15a861fab83818441

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_95000_tau0.1_entry12",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_95000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 271,
    "estimator": "fk",
    "runtime": true,
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
    }
  },
  "checkpoint_sha256": "a9ca81d693e2ee34f29bbb8746ae6c7a09f1a201d1d579d15a861fab83818441",
  "onnx_sha256": "7e9315ab3ff8de6c69ba7599d9f20f2c432877c181d5c6228d4b55646de7b449",
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
  "initial_physics_sha256": "a69492bdb4f4a37bc2982ad18fdf4cca85ab984657c0e32367b5b85236a2ece6",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.022449815740468997,
  "max_drift_m": 0.0545663269089523,
  "radial_IAE_m_s": 1.347523609950068,
  "signed_longitudinal_delta_m": -0.022443880139245646,
  "tail_speed_mean_m_s": 7.627934679674795e-07,
  "tail_speed_rms_m_s": 7.638344150255917e-07,
  "tail_sensor_speed_mean_m_s": 1.0288800495344993e-06,
  "tail_fk_speed_mean_m_s": 3.983685800430986e-07,
  "peak_tilt_rad": 0.08262074586426849,
  "peak_wheel_torque_nm": 0.555385947227478,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.23715712877701198,
  "final_integral_m_s": -0.23715792067456232,
  "elapsed_wall_s": 14.11251976096537
}
```
