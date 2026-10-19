# tita_flash_sac_193248_068255_model_20000_friction02_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 4bb0e92e03390c3256497280f4ab3eda89d64ce8dfc23bfd9d799d69aa0d068c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_20000_friction02_baseline_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_20000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "friction": 0.2
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "4bb0e92e03390c3256497280f4ab3eda89d64ce8dfc23bfd9d799d69aa0d068c",
  "onnx_sha256": "a24d51f2c61ac25fc44c8e657cd90494575b17855d820a382e66b027caddbaac",
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
  "initial_physics_sha256": "0d0d9b0a60b4b6acc8acbc5ae14cda6272a61448c4392ff9921cd4dc1df0797f",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 7.787561365938596,
  "max_drift_m": 7.787561365938596,
  "radial_IAE_m_s": 296.7738450866338,
  "signed_longitudinal_delta_m": -1.465471193260785,
  "tail_speed_mean_m_s": 0.20828001195009782,
  "tail_speed_rms_m_s": 0.20828001198876253,
  "tail_sensor_speed_mean_m_s": 0.20869132508507096,
  "tail_fk_speed_mean_m_s": 0.2087762100600496,
  "peak_tilt_rad": 0.15306784865810963,
  "peak_wheel_torque_nm": 0.10177457332611084,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 12.688084699038882
}
```
