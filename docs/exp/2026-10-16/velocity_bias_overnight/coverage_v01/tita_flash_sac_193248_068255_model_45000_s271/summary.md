# tita_flash_sac_193248_068255_model_45000_s271

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 70a9e97ecbd4861ec30c17805a0e137ff6f7723b96433205dbd8c3fc0e1b103a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_45000_s271",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_45000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 271,
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.05,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
    },
    "estimator": "fk"
  },
  "checkpoint_sha256": "70a9e97ecbd4861ec30c17805a0e137ff6f7723b96433205dbd8c3fc0e1b103a",
  "onnx_sha256": "f6bd5f1e2f31278db9eb7cc34e33c35b26407a27d2b9d587a0443c3dc0ab4bb8",
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
  "initial_physics_sha256": "42a41b2d61b6cff6833d67bc947fde8bd7941229c4adee412a50ca5bf41ee96c",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.019310466021007507,
  "max_drift_m": 0.05738088727205827,
  "radial_IAE_m_s": 1.21070301200978,
  "signed_longitudinal_delta_m": -0.019308788319730524,
  "tail_speed_mean_m_s": 1.6948238288199368e-05,
  "tail_speed_rms_m_s": 1.6948777059743585e-05,
  "tail_sensor_speed_mean_m_s": 1.7875510323448295e-05,
  "tail_fk_speed_mean_m_s": 1.5392117261563043e-05,
  "peak_tilt_rad": 0.10144181062901692,
  "peak_wheel_torque_nm": 0.9297584295272827,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.21195187293811346,
  "final_integral_m_s": -0.2119822133074988,
  "elapsed_wall_s": 4.4255407609744
}
```
