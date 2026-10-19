# tita_flash_sac_193248_068255_model_95000_com_plus5mm_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a9ca81d693e2ee34f29bbb8746ae6c7a09f1a201d1d579d15a861fab83818441

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_95000_com_plus5mm_baseline_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_95000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "com": 0.005
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
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
  "initial_physics_sha256": "804ba4b134fe114f7f07a299d7ca42cce1bcdec22ea56ab3764e292734be2110",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.9579883543998993,
  "max_drift_m": 0.9579883543998993,
  "radial_IAE_m_s": 32.53664846146241,
  "signed_longitudinal_delta_m": -0.9579642526854518,
  "tail_speed_mean_m_s": -0.01309387641303869,
  "tail_speed_rms_m_s": 0.013097894972954586,
  "tail_sensor_speed_mean_m_s": -0.01306507438637546,
  "tail_fk_speed_mean_m_s": -0.01306554689239317,
  "peak_tilt_rad": 0.05998725004525607,
  "peak_wheel_torque_nm": 0.2714587450027466,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 13.684409743989818
}
```
