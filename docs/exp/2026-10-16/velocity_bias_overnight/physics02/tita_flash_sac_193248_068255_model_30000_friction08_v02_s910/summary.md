# tita_flash_sac_193248_068255_model_30000_friction08_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 1e8eb8c4549e7335f4ef3d31ec9b7b45fd0cb148283a41b8c616f429cefb643f

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_30000_friction08_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_30000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "friction": 0.8
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
  "checkpoint_sha256": "1e8eb8c4549e7335f4ef3d31ec9b7b45fd0cb148283a41b8c616f429cefb643f",
  "onnx_sha256": "ec18f72b80fd3755cb0dce2de3434e16c4375a38100a8a08c28560539614d4a8",
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
  "initial_physics_sha256": "2ba90a74aac663a632b172cb58cb33a544ad97112e1471a8afb2f807f02ca5cd",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.010665870277175086,
  "max_drift_m": 0.01763015229587135,
  "radial_IAE_m_s": 0.6410580170498958,
  "signed_longitudinal_delta_m": 0.010662353392288895,
  "tail_speed_mean_m_s": 4.412425388512485e-07,
  "tail_speed_rms_m_s": 4.680585911401829e-07,
  "tail_sensor_speed_mean_m_s": 6.87458696813033e-07,
  "tail_fk_speed_mean_m_s": 3.71525361945376e-07,
  "peak_tilt_rad": 0.01996019690874795,
  "peak_wheel_torque_nm": 0.36211296916007996,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.11080032242181652,
  "final_integral_m_s": 0.11080002107546265,
  "elapsed_wall_s": 23.203165451006498
}
```
