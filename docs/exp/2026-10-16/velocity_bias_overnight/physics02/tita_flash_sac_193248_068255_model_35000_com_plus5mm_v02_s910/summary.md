# tita_flash_sac_193248_068255_model_35000_com_plus5mm_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 29db772e13dbcedf2c18de4abb1574229f1744fb03a20ccba615236d504773ae

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_35000_com_plus5mm_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_35000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "com": 0.005
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
  "initial_physics_sha256": "b46c15ec6eb9f164ab038148a3f2ff1c90589aca7ac5e414a36c6a081712ec59",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.03252485169124107,
  "max_drift_m": 0.04527858641740155,
  "radial_IAE_m_s": 1.8940648113327252,
  "signed_longitudinal_delta_m": 0.03252482107153825,
  "tail_speed_mean_m_s": 3.1697864130090866e-05,
  "tail_speed_rms_m_s": 3.2087736974729784e-05,
  "tail_sensor_speed_mean_m_s": 3.1433523476080004e-05,
  "tail_fk_speed_mean_m_s": 3.06236904506875e-05,
  "peak_tilt_rad": 0.06330973291396202,
  "peak_wheel_torque_nm": 0.7829123735427856,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.3364149228675209,
  "final_integral_m_s": 0.3363621926653639,
  "elapsed_wall_s": 19.040819283982273
}
```
