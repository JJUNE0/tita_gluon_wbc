# tita_flash_sac_193248_068255_model_95000

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a9ca81d693e2ee34f29bbb8746ae6c7a09f1a201d1d579d15a861fab83818441

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_95000",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_95000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 270,
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
  "initial_physics_sha256": "952e9fe19f78d7f53dfd5288895ca7b16dc55c80b1cb69c4b93375973af3d71e",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 8.982711162001785,
  "max_drift_m": 8.982711162001785,
  "radial_IAE_m_s": 242.1169677550035,
  "signed_longitudinal_delta_m": -8.689195454152502,
  "tail_speed_mean_m_s": -0.19080544383842818,
  "tail_speed_rms_m_s": 0.1921419980922349,
  "tail_sensor_speed_mean_m_s": -0.19055427025498478,
  "tail_fk_speed_mean_m_s": -0.1905819354027496,
  "peak_tilt_rad": 0.03971393078547947,
  "peak_wheel_torque_nm": 0.07179230451583862,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 5.20423368900083
}
```
