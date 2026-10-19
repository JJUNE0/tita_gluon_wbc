# tita_flash_sac_193248_068255_model_45000_friction0.8_v01

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 70a9e97ecbd4861ec30c17805a0e137ff6f7723b96433205dbd8c3fc0e1b103a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_45000_friction0.8_v01",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_45000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 272,
    "physics": {
      "friction": 0.8
    },
    "kick": 0.0,
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
  "initial_physics_sha256": "3c665836365afffd4bc748f3e5a5d0899250615262d5d1192ef855944f6149e6",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.020261499309389537,
  "max_drift_m": 0.060093014256821266,
  "radial_IAE_m_s": 1.2818733807865963,
  "signed_longitudinal_delta_m": -0.02025503569837012,
  "tail_speed_mean_m_s": 2.470434083802451e-05,
  "tail_speed_rms_m_s": 2.4708066015349628e-05,
  "tail_sensor_speed_mean_m_s": 2.078349778090167e-05,
  "tail_fk_speed_mean_m_s": 1.7196400348234798e-05,
  "peak_tilt_rad": 0.1038791737510043,
  "peak_wheel_torque_nm": 0.9703126549720764,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.22601950870502566,
  "final_integral_m_s": -0.22605375933908095,
  "elapsed_wall_s": 5.558430289034732
}
```
