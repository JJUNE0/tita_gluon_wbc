# tita_flash_sac_193248_068255_model_95000_com_minus5mm_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a9ca81d693e2ee34f29bbb8746ae6c7a09f1a201d1d579d15a861fab83818441

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_95000_com_minus5mm_baseline_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_95000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "com": -0.005
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
  "initial_physics_sha256": "0451442c5c5ba3de94a9f611f17ae46f3380be106184aa440e0293324528765d",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 15.027047684707211,
  "max_drift_m": 15.027047684707211,
  "radial_IAE_m_s": 440.2872314771312,
  "signed_longitudinal_delta_m": -14.381724945575018,
  "tail_speed_mean_m_s": -0.25959277897861144,
  "tail_speed_rms_m_s": 0.25960512327998364,
  "tail_sensor_speed_mean_m_s": -0.2591853494295864,
  "tail_fk_speed_mean_m_s": -0.2591964673023961,
  "peak_tilt_rad": 0.03628092806698424,
  "peak_wheel_torque_nm": 0.22329866886138916,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 16.138718213012908
}
```
