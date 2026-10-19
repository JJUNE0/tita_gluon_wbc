# tita_flash_sac_193248_068255_model_20000_friction02_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 4bb0e92e03390c3256497280f4ab3eda89d64ce8dfc23bfd9d799d69aa0d068c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_20000_friction02_v04_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_20000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
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
      "slew": 3.0,
      "seed_gain": 3.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
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
  "initial_physics_sha256": "aa7fff271c43db1099c898fcb347e4143e5e9c27f168f447f8a7d52bc4c66691",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.025358251885910475,
  "max_drift_m": 0.0688374102409167,
  "radial_IAE_m_s": 1.1534942669002335,
  "signed_longitudinal_delta_m": 0.011677908359187921,
  "tail_speed_mean_m_s": -0.0005055693049384048,
  "tail_speed_rms_m_s": 0.0005055695048903499,
  "tail_sensor_speed_mean_m_s": -0.00010926156032211005,
  "tail_fk_speed_mean_m_s": -1.3810020273921848e-07,
  "peak_tilt_rad": 0.1379701047637405,
  "peak_wheel_torque_nm": 1.6618887186050415,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.6685862608104853,
  "final_integral_m_s": 0.6685862608104853,
  "elapsed_wall_s": 9.51197398698423
}
```
