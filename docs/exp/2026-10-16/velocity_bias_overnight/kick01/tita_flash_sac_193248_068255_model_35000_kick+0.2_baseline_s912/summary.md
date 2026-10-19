# tita_flash_sac_193248_068255_model_35000_kick+0.2_baseline_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 29db772e13dbcedf2c18de4abb1574229f1744fb03a20ccba615236d504773ae

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_35000_kick+0.2_baseline_s912",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_35000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 912,
    "estimator": "fk",
    "runtime": false,
    "kick": 0.2,
    "law": {
      "mode": "constant",
      "bias": 0.0
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
  "initial_physics_sha256": "9fa8d10a0b56c44d3f9642cef45445a937a2760d786c6536359d7482f99bec73",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 8.804699837572404,
  "max_drift_m": 8.804699837572404,
  "radial_IAE_m_s": 259.62386287804645,
  "signed_longitudinal_delta_m": 8.704454538904791,
  "tail_speed_mean_m_s": 0.1546434537751405,
  "tail_speed_rms_m_s": 0.15465079691483657,
  "tail_sensor_speed_mean_m_s": 0.15431020970728035,
  "tail_fk_speed_mean_m_s": 0.1542936995999084,
  "peak_tilt_rad": 0.08911109123339322,
  "peak_wheel_torque_nm": 1.4000409841537476,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 12.581155679014046
}
```
