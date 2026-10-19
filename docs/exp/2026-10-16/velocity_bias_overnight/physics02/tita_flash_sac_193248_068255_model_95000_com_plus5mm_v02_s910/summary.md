# tita_flash_sac_193248_068255_model_95000_com_plus5mm_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a9ca81d693e2ee34f29bbb8746ae6c7a09f1a201d1d579d15a861fab83818441

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_95000_com_plus5mm_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_95000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "com": 0.005
    },
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
  "initial_physics_sha256": "804ba4b134fe114f7f07a299d7ca42cce1bcdec22ea56ab3764e292734be2110",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.003596997083232157,
  "max_drift_m": 0.029979396194545472,
  "radial_IAE_m_s": 0.2616401312697354,
  "signed_longitudinal_delta_m": -0.003577631013613245,
  "tail_speed_mean_m_s": 5.302568993792196e-06,
  "tail_speed_rms_m_s": 6.008415052450193e-06,
  "tail_sensor_speed_mean_m_s": 5.534540313133165e-06,
  "tail_fk_speed_mean_m_s": 5.0286503539137084e-06,
  "peak_tilt_rad": 0.07091434629761495,
  "peak_wheel_torque_nm": 0.35181736946105957,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.044298750091209434,
  "final_integral_m_s": -0.04431666332973548,
  "elapsed_wall_s": 17.209992157993838
}
```
