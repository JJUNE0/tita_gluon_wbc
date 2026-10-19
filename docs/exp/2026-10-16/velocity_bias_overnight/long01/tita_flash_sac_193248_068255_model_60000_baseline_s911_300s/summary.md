# tita_flash_sac_193248_068255_model_60000_baseline_s911_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 9b0d8897472dc567619d49df3e6df08813dcbb15b018f23ed58060e92e1b139b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_60000_baseline_s911_300s",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_60000",
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
  "checkpoint_sha256": "9b0d8897472dc567619d49df3e6df08813dcbb15b018f23ed58060e92e1b139b",
  "onnx_sha256": "bd80a0d28ffd69209d8e2ef2f6d867ca3f72a00abd0a3c8dbb0b6def13e19b7e",
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
  "initial_physics_sha256": "92ee2659ac20f3135e8a2ec13865cef4b86a3b1eebd246135b650acfbd5c4b02",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.8680104430797416,
  "max_drift_m": 0.8680104430797416,
  "radial_IAE_m_s": 93.17819236824336,
  "signed_longitudinal_delta_m": 0.8204375431128963,
  "tail_speed_mean_m_s": 0.008819750040232015,
  "tail_speed_rms_m_s": 0.008820643090016898,
  "tail_sensor_speed_mean_m_s": 0.008800668904276247,
  "tail_fk_speed_mean_m_s": 0.008801811464552315,
  "peak_tilt_rad": 0.035418095286237294,
  "peak_wheel_torque_nm": 0.09932301938533783,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 64.21509759902256
}
```
