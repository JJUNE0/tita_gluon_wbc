# tita_flash_sac_193248_068255_model_45000_friction0.8_baseline

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 70a9e97ecbd4861ec30c17805a0e137ff6f7723b96433205dbd8c3fc0e1b103a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_45000_friction0.8_baseline",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_45000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 272,
    "physics": {
      "friction": 0.8
    },
    "kick": 0.0,
    "law": {
      "mode": "constant",
      "bias": 0.0
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
  "final_drift_m": 8.818232015015738,
  "max_drift_m": 8.818232015015738,
  "radial_IAE_m_s": 261.3556799576998,
  "signed_longitudinal_delta_m": -8.627301380774917,
  "tail_speed_mean_m_s": -0.15340090595936742,
  "tail_speed_rms_m_s": 0.15341059240199922,
  "tail_sensor_speed_mean_m_s": -0.15318203262286884,
  "tail_fk_speed_mean_m_s": -0.15320614928865497,
  "peak_tilt_rad": 0.024803095314462453,
  "peak_wheel_torque_nm": 0.07118338346481323,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 5.47092445299495
}
```
