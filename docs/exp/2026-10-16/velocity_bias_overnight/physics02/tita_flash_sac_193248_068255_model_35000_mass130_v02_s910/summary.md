# tita_flash_sac_193248_068255_model_35000_mass130_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 29db772e13dbcedf2c18de4abb1574229f1744fb03a20ccba615236d504773ae

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_35000_mass130_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_35000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "mass": 1.3
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
  "checkpoint_sha256": "29db772e13dbcedf2c18de4abb1574229f1744fb03a20ccba615236d504773ae",
  "onnx_sha256": "a1536d3d580cb29e5617b2c1b7c4a7caef45b7730f864b35d9d082a39fc4ebd6",
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
  "initial_physics_sha256": "1273387a48e36e30405337203b0fc15d336564bc8aac860d066a6c1650a1bdfd",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.03400908073009282,
  "max_drift_m": 0.04965149244102174,
  "radial_IAE_m_s": 2.0812110880493426,
  "signed_longitudinal_delta_m": -0.03400519703186778,
  "tail_speed_mean_m_s": 2.06811972622911e-05,
  "tail_speed_rms_m_s": 2.0688889771088435e-05,
  "tail_sensor_speed_mean_m_s": 2.0486615127431112e-05,
  "tail_fk_speed_mean_m_s": 2.0002522786280983e-05,
  "peak_tilt_rad": 0.12008572401280015,
  "peak_wheel_torque_nm": 1.3163995742797852,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.3535604601540452,
  "final_integral_m_s": -0.3535985177109061,
  "elapsed_wall_s": 22.230496698000934
}
```
