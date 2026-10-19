# tita_flash_sac_193248_068255_model_20000_friction02_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 4bb0e92e03390c3256497280f4ab3eda89d64ce8dfc23bfd9d799d69aa0d068c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_20000_friction02_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_20000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "friction": 0.2
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
  "initial_physics_sha256": "0d0d9b0a60b4b6acc8acbc5ae14cda6272a61448c4392ff9921cd4dc1df0797f",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.05226534539328927,
  "max_drift_m": 0.08030887503765816,
  "radial_IAE_m_s": 3.1271170632138436,
  "signed_longitudinal_delta_m": 0.04838834666982636,
  "tail_speed_mean_m_s": -0.0005055079489611619,
  "tail_speed_rms_m_s": 0.0005055079952953548,
  "tail_sensor_speed_mean_m_s": -0.00010920412741374582,
  "tail_fk_speed_mean_m_s": -8.266407771211528e-08,
  "peak_tilt_rad": 0.13818242815324,
  "peak_wheel_torque_nm": 1.8005985021591187,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.6685844371693841,
  "final_integral_m_s": 0.6685838225516733,
  "elapsed_wall_s": 16.018739366030786
}
```
