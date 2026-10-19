# tita_flash_sac_193248_068255_model_95000_v02_s911_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a9ca81d693e2ee34f29bbb8746ae6c7a09f1a201d1d579d15a861fab83818441

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_95000_v02_s911_300s",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_95000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 911,
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
  "initial_physics_sha256": "b6a81f9e83e063ea6641a09c590df2f20d440e994886d07b86c9542414f84ee6",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.02199593469500282,
  "max_drift_m": 0.05456633775075216,
  "radial_IAE_m_s": 6.680886923342772,
  "signed_longitudinal_delta_m": -0.02199442501530332,
  "tail_speed_mean_m_s": 1.8486746158394436e-06,
  "tail_speed_rms_m_s": 1.8489286917586e-06,
  "tail_sensor_speed_mean_m_s": 1.974322743131748e-06,
  "tail_fk_speed_mean_m_s": 1.379359431347375e-06,
  "peak_tilt_rad": 0.08262073987291552,
  "peak_wheel_torque_nm": 0.555388331413269,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.23331599486386279,
  "final_integral_m_s": -0.2333187111150838,
  "elapsed_wall_s": 71.48106150497915
}
```
