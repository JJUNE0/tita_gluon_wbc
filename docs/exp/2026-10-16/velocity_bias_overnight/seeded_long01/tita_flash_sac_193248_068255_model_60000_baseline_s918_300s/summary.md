# tita_flash_sac_193248_068255_model_60000_baseline_s918_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 9b0d8897472dc567619d49df3e6df08813dcbb15b018f23ed58060e92e1b139b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_60000_baseline_s918_300s",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_60000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 918,
    "estimator": "fk",
    "guarded": false,
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
  },
  "checkpoint_sha256": "9b0d8897472dc567619d49df3e6df08813dcbb15b018f23ed58060e92e1b139b",
  "onnx_sha256": "bd80a0d28ffd69209d8e2ef2f6d867ca3f72a00abd0a3c8dbb0b6def13e19b7e",
  "input_columns": [
    "velocity_bias_m_s",
    "filtered_velocity_m_s",
    "integral_m_s"
  ],
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
  "initial_physics_sha256": "50685a706564416fca2fd3ae10125b2cbef9eb38dde925377f76c72628b19542",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.8181911005895206,
  "max_drift_m": 0.8181911005895206,
  "radial_IAE_m_s": 93.11574732582196,
  "signed_longitudinal_delta_m": 0.7689965309968722,
  "tail_speed_mean_m_s": 0.008754618491165277,
  "tail_speed_rms_m_s": 0.008755539402208986,
  "tail_sensor_speed_mean_m_s": 0.008735689026807332,
  "tail_fk_speed_mean_m_s": 0.008736835614114811,
  "peak_tilt_rad": 0.03541828834253091,
  "peak_wheel_torque_nm": 0.09894034266471863,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 44.8797611760092
}
```
