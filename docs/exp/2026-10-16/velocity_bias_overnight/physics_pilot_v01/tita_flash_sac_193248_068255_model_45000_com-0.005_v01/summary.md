# tita_flash_sac_193248_068255_model_45000_com-0.005_v01

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 70a9e97ecbd4861ec30c17805a0e137ff6f7723b96433205dbd8c3fc0e1b103a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_45000_com-0.005_v01",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_45000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 272,
    "physics": {
      "com": -0.005
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
  "initial_physics_sha256": "e66d68dbbcd457edbae379880ac87a33964efebb9a21af14c3465d1b4669dd07",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.02452737635454965,
  "max_drift_m": 0.07067505651507461,
  "radial_IAE_m_s": 1.5240067079848139,
  "signed_longitudinal_delta_m": -0.024522970248801262,
  "tail_speed_mean_m_s": 1.5973706109990412e-05,
  "tail_speed_rms_m_s": 1.5977857260978123e-05,
  "tail_sensor_speed_mean_m_s": 1.6758189730023804e-05,
  "tail_fk_speed_mean_m_s": 1.407742053506245e-05,
  "peak_tilt_rad": 0.11377184767886317,
  "peak_wheel_torque_nm": 1.214728593826294,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.2679940348343884,
  "final_integral_m_s": -0.2680219618951313,
  "elapsed_wall_s": 5.477185346942861
}
```
