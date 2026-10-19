# tita_flash_sac_193248_068255_model_35000_raw_s271

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 29db772e13dbcedf2c18de4abb1574229f1744fb03a20ccba615236d504773ae

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_35000_raw_s271",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_35000",
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
    "estimator": "raw"
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
  "initial_physics_sha256": "0b051c5adf72d89865b52f29154073a480b030a21a52034bae21358fb5670226",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.015704820541662605,
  "max_drift_m": 0.04979183957066922,
  "radial_IAE_m_s": 1.3821632397008181,
  "signed_longitudinal_delta_m": 0.015677781790307592,
  "tail_speed_mean_m_s": -0.00033872576669709476,
  "tail_speed_rms_m_s": 0.027057204719065794,
  "tail_sensor_speed_mean_m_s": -0.0005700399626468478,
  "tail_fk_speed_mean_m_s": -0.00012844309646284813,
  "peak_tilt_rad": 0.06433680349136872,
  "peak_wheel_torque_nm": 1.6262704133987427,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.04939593593607686,
  "final_integral_m_s": 0.11390831183339102,
  "elapsed_wall_s": 4.295466126990505
}
```
