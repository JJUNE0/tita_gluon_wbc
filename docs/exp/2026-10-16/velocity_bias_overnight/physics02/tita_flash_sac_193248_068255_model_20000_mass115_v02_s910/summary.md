# tita_flash_sac_193248_068255_model_20000_mass115_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 4bb0e92e03390c3256497280f4ab3eda89d64ce8dfc23bfd9d799d69aa0d068c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_20000_mass115_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_20000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "mass": 1.15
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
  "final_drift_m": 0.015199492147281805,
  "max_drift_m": 0.028407300516783595,
  "radial_IAE_m_s": 0.9200633088688057,
  "signed_longitudinal_delta_m": 0.015189931684516428,
  "tail_speed_mean_m_s": -1.8179322113018847e-06,
  "tail_speed_rms_m_s": 1.8295503860233974e-06,
  "tail_sensor_speed_mean_m_s": -1.7320409990170957e-06,
  "tail_fk_speed_mean_m_s": 1.0387410014506366e-06,
  "peak_tilt_rad": 0.14467083154805205,
  "peak_wheel_torque_nm": 1.171574592590332,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.16323938779681815,
  "final_integral_m_s": 0.16323752649712464,
  "elapsed_wall_s": 15.493327067000791
}
```
