# tita_flash_sac_193248_068255_model_50000_v02_s911_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 948c108cb4740ede74b9c33fdca02f3a0bc4ae70aeb862e20f90c841243b1087

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_50000_v02_s911_300s",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_50000",
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
  "checkpoint_sha256": "948c108cb4740ede74b9c33fdca02f3a0bc4ae70aeb862e20f90c841243b1087",
  "onnx_sha256": "9edc5ad830f2e0f0d88dcb9bd8a21a023d3cdd754ce2e54339650dc66d2bb1c4",
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
  "initial_physics_sha256": "8bdf1eef6b5eb6f3f28b8639db05301ed998ad8f516f4093de22a2e40061027f",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.06778566172505573,
  "max_drift_m": 0.06931315189241519,
  "radial_IAE_m_s": 20.44797881050121,
  "signed_longitudinal_delta_m": 0.06778324316672753,
  "tail_speed_mean_m_s": 1.6662317663649775e-06,
  "tail_speed_rms_m_s": 4.335395269434599e-06,
  "tail_sensor_speed_mean_m_s": 1.1956531198880473e-06,
  "tail_fk_speed_mean_m_s": 1.9565881158868645e-06,
  "peak_tilt_rad": 0.050760948161947095,
  "peak_wheel_torque_nm": 0.6503066420555115,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.6866533291751609,
  "final_integral_m_s": 0.6866650327230421,
  "elapsed_wall_s": 79.83199227502337
}
```
