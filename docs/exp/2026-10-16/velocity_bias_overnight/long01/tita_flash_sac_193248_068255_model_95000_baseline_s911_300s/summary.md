# tita_flash_sac_193248_068255_model_95000_baseline_s911_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a9ca81d693e2ee34f29bbb8746ae6c7a09f1a201d1d579d15a861fab83818441

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_95000_baseline_s911_300s",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_95000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 911,
    "estimator": "fk",
    "runtime": false,
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "a9ca81d693e2ee34f29bbb8746ae6c7a09f1a201d1d579d15a861fab83818441",
  "onnx_sha256": "7e9315ab3ff8de6c69ba7599d9f20f2c432877c181d5c6228d4b55646de7b449",
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
  "initial_physics_sha256": "b6a81f9e83e063ea6641a09c590df2f20d440e994886d07b86c9542414f84ee6",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 13.401910574660295,
  "max_drift_m": 20.83281912923395,
  "radial_IAE_m_s": 3367.4306250247064,
  "signed_longitudinal_delta_m": -12.128814956168402,
  "tail_speed_mean_m_s": -0.28581237216567223,
  "tail_speed_rms_m_s": 0.28581237217060657,
  "tail_sensor_speed_mean_m_s": -0.285413153746893,
  "tail_fk_speed_mean_m_s": -0.2854684987655466,
  "peak_tilt_rad": 0.04487232132409469,
  "peak_wheel_torque_nm": 0.22539913654327393,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 60.40314508404117
}
```
