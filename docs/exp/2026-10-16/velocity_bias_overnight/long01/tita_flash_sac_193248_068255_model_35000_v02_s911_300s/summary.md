# tita_flash_sac_193248_068255_model_35000_v02_s911_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 29db772e13dbcedf2c18de4abb1574229f1744fb03a20ccba615236d504773ae

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_35000_v02_s911_300s",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_35000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 911,
    "estimator": "fk",
    "runtime": true,
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
  "initial_physics_sha256": "98f08d08701ac4c2ecdb733b569df7a1980d7f1365eb5d489f5f0d1cff725f47",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.03376765429672544,
  "max_drift_m": 0.03822226920686909,
  "radial_IAE_m_s": 9.526144096927867,
  "signed_longitudinal_delta_m": 0.033743378920470656,
  "tail_speed_mean_m_s": 3.540850948987978e-06,
  "tail_speed_rms_m_s": 3.5443075030006458e-06,
  "tail_sensor_speed_mean_m_s": 4.1903233024652044e-06,
  "tail_fk_speed_mean_m_s": 2.446260308725935e-06,
  "peak_tilt_rad": 0.05827888158546379,
  "peak_wheel_torque_nm": 0.6241953372955322,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.3442137577576423,
  "final_integral_m_s": 0.34420934125781383,
  "elapsed_wall_s": 76.05856788094388
}
```
