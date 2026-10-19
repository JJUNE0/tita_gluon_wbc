# tita_flash_sac_193248_068255_model_20000_mass115_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 4bb0e92e03390c3256497280f4ab3eda89d64ce8dfc23bfd9d799d69aa0d068c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_20000_mass115_baseline_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_20000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "mass": 1.15
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
  "initial_physics_sha256": "451e9a1071cc2a8911686c41910a4f47df0eb9476be5f5300c74c64e14f5b48b",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 4.467414650177213,
  "max_drift_m": 4.467414650177213,
  "radial_IAE_m_s": 134.2917393701212,
  "signed_longitudinal_delta_m": 4.466762611132756,
  "tail_speed_mean_m_s": 0.07415898161294934,
  "tail_speed_rms_m_s": 0.07415899530047429,
  "tail_sensor_speed_mean_m_s": 0.0740001892080223,
  "tail_fk_speed_mean_m_s": 0.07399986064045942,
  "peak_tilt_rad": 0.147011686091028,
  "peak_wheel_torque_nm": 0.379711389541626,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 14.831286641012412
}
```
