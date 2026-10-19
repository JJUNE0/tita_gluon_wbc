# tita_flash_sac_193248_068255_model_95000_kick-0.2_v02_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a9ca81d693e2ee34f29bbb8746ae6c7a09f1a201d1d579d15a861fab83818441

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_95000_kick-0.2_v02_s912",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_95000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 912,
    "estimator": "fk",
    "runtime": true,
    "kick": -0.2,
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
  "initial_physics_sha256": "d75dee25ee7f6ed348bf419046907d26ccdda1e736ecb5b554bf6801213f98df",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.3908107417468621,
  "max_drift_m": 0.8965866548459366,
  "radial_IAE_m_s": 20.094152216302266,
  "signed_longitudinal_delta_m": 0.38863662456791204,
  "tail_speed_mean_m_s": -0.004610817115298369,
  "tail_speed_rms_m_s": 0.365140107645087,
  "tail_sensor_speed_mean_m_s": -0.006935744850181534,
  "tail_fk_speed_mean_m_s": -0.004506312937831238,
  "peak_tilt_rad": 0.219256178930195,
  "peak_wheel_torque_nm": 3.2973413467407227,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -1.6309459750989361,
  "final_integral_m_s": -1.7921042173742507,
  "elapsed_wall_s": 12.00805845897412
}
```
