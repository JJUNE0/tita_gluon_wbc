# tita_flash_sac_193248_068255_model_90000_kick+0.2_baseline_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d94ec425dcab69bfb8001711468b6ca37297f4e1aec2e9b20535fd106ee98769

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_90000_kick+0.2_baseline_s912",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_90000",
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
  "initial_physics_sha256": "2ba987a3c588be043dc77a7e97bd440dfee1c62fbe4b24ed8f32cd43a6acbadf",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 13.342482886544927,
  "max_drift_m": 13.342482886544927,
  "radial_IAE_m_s": 400.60261237854485,
  "signed_longitudinal_delta_m": 13.33466282606855,
  "tail_speed_mean_m_s": 0.22359430339430036,
  "tail_speed_rms_m_s": 0.22359438853270705,
  "tail_sensor_speed_mean_m_s": 0.22311064434724423,
  "tail_fk_speed_mean_m_s": 0.22310830882817229,
  "peak_tilt_rad": 0.1143283448586292,
  "peak_wheel_torque_nm": 1.2293415069580078,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 8.12832131399773
}
```
