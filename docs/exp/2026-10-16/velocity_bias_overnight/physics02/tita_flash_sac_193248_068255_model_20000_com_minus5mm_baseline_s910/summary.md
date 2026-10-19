# tita_flash_sac_193248_068255_model_20000_com_minus5mm_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 4bb0e92e03390c3256497280f4ab3eda89d64ce8dfc23bfd9d799d69aa0d068c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_20000_com_minus5mm_baseline_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_20000",
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
  "initial_physics_sha256": "80afd21098615a31ac96e6a608b4d4f12bf9ab804e00f6474b82e0771cc3578f",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 12.191842025824496,
  "max_drift_m": 12.191842025824496,
  "radial_IAE_m_s": 365.78919579035613,
  "signed_longitudinal_delta_m": 12.163307049515563,
  "tail_speed_mean_m_s": 0.20446242990500413,
  "tail_speed_rms_m_s": 0.20446243013176557,
  "tail_sensor_speed_mean_m_s": 0.20402118082681864,
  "tail_fk_speed_mean_m_s": 0.20400981711545021,
  "peak_tilt_rad": 0.15359224926832016,
  "peak_wheel_torque_nm": 0.4579341411590576,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 13.048689544026274
}
```
