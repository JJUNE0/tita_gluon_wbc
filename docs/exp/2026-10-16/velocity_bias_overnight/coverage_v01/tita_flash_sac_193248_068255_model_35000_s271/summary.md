# tita_flash_sac_193248_068255_model_35000_s271

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 29db772e13dbcedf2c18de4abb1574229f1744fb03a20ccba615236d504773ae

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_35000_s271",
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
    "estimator": "fk"
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
  "final_drift_m": 0.02969503641927874,
  "max_drift_m": 0.050785208475810036,
  "radial_IAE_m_s": 1.7418794856671072,
  "signed_longitudinal_delta_m": 0.029694762706494557,
  "tail_speed_mean_m_s": 2.8614477195839315e-05,
  "tail_speed_rms_m_s": 2.8618049938842683e-05,
  "tail_sensor_speed_mean_m_s": 2.830647108329283e-05,
  "tail_fk_speed_mean_m_s": 2.733818667196354e-05,
  "peak_tilt_rad": 0.06433680349136872,
  "peak_wheel_torque_nm": 1.2455281019210815,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.3136993097662939,
  "final_integral_m_s": 0.31364662644460034,
  "elapsed_wall_s": 4.3778379609575495
}
```
