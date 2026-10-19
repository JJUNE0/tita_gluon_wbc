# tita_flash_sac_193248_068255_model_90000_v02_s911_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d94ec425dcab69bfb8001711468b6ca37297f4e1aec2e9b20535fd106ee98769

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_90000_v02_s911_300s",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_90000",
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
  "checkpoint_sha256": "d94ec425dcab69bfb8001711468b6ca37297f4e1aec2e9b20535fd106ee98769",
  "onnx_sha256": "aff309a07b913000eb7916a9b3867232296f7834f48d5391c16e7ec4e09b84d2",
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
  "initial_physics_sha256": "66523d4c2ed3c9157748d5502fb99b001d89b00a53b9c58b722faa973a980a93",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.0704775473452317,
  "max_drift_m": 0.07479421123726214,
  "radial_IAE_m_s": 19.924892426680913,
  "signed_longitudinal_delta_m": 0.07047702210576366,
  "tail_speed_mean_m_s": 1.1204348910291972e-06,
  "tail_speed_rms_m_s": 6.8743921268312555e-06,
  "tail_sensor_speed_mean_m_s": 5.901633708998737e-06,
  "tail_fk_speed_mean_m_s": 1.0870120741627856e-05,
  "peak_tilt_rad": 0.10173462920981269,
  "peak_wheel_torque_nm": 1.9213157892227173,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.7151546082932405,
  "final_integral_m_s": 0.7151399315587216,
  "elapsed_wall_s": 81.1897960480419
}
```
