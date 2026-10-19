# tita_flash_sac_193248_068255_model_35000_friction08_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 29db772e13dbcedf2c18de4abb1574229f1744fb03a20ccba615236d504773ae

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_35000_friction08_baseline_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_35000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "friction": 0.8
    },
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
  "initial_physics_sha256": "51db59d0c7809e2f9db1b5d7e9e28da35cf600af25f682e5b77d89604feb18b9",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 8.406000589055427,
  "max_drift_m": 8.406000589055427,
  "radial_IAE_m_s": 241.40996704748517,
  "signed_longitudinal_delta_m": 8.366660372467837,
  "tail_speed_mean_m_s": 0.15207344959472427,
  "tail_speed_rms_m_s": 0.15208561094722117,
  "tail_sensor_speed_mean_m_s": 0.15174538240802068,
  "tail_fk_speed_mean_m_s": 0.1517293795947768,
  "peak_tilt_rad": 0.07055858591885333,
  "peak_wheel_torque_nm": 0.1261310577392578,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 13.923318868968636
}
```
