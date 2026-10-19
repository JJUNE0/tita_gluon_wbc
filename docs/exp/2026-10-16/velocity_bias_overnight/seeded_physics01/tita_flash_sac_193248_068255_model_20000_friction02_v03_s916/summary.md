# tita_flash_sac_193248_068255_model_20000_friction02_v03_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 4bb0e92e03390c3256497280f4ab3eda89d64ce8dfc23bfd9d799d69aa0d068c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_20000_friction02_v03_s916",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_20000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "friction": 0.2
    },
    "law": {
      "kp": 0.0,
      "ki": 4.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0,
      "seed_gain": 3.0
    },
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
  },
  "checkpoint_sha256": "4bb0e92e03390c3256497280f4ab3eda89d64ce8dfc23bfd9d799d69aa0d068c",
  "onnx_sha256": "a24d51f2c61ac25fc44c8e657cd90494575b17855d820a382e66b027caddbaac",
  "input_columns": [
    "velocity_bias_m_s",
    "filtered_velocity_m_s",
    "integral_m_s"
  ],
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
  "initial_physics_sha256": "cf8a929a8ad5e45b2b76539b9cc73891e7e1db8b0bce850e1242c8b5f7d8791f",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.02614180498949167,
  "max_drift_m": 0.07634136068446126,
  "radial_IAE_m_s": 1.1867725119125572,
  "signed_longitudinal_delta_m": 0.011547791314129505,
  "tail_speed_mean_m_s": -0.0005055653721639782,
  "tail_speed_rms_m_s": 0.0005055655786038386,
  "tail_sensor_speed_mean_m_s": -0.0001092544479258057,
  "tail_fk_speed_mean_m_s": -1.3427838625469725e-07,
  "peak_tilt_rad": 0.1379776479317052,
  "peak_wheel_torque_nm": 1.5745861530303955,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.6685868146555709,
  "final_integral_m_s": 0.6685868146555709,
  "elapsed_wall_s": 10.41240326501429
}
```
