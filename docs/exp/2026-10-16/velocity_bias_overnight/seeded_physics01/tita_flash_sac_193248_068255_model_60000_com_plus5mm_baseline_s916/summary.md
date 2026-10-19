# tita_flash_sac_193248_068255_model_60000_com_plus5mm_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 9b0d8897472dc567619d49df3e6df08813dcbb15b018f23ed58060e92e1b139b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_60000_com_plus5mm_baseline_s916",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_60000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "com": 0.005
    },
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
  "initial_physics_sha256": "8ab23aad5fadc6dc76331b7eae3d8a7f5c865e8cb7679eb90a5b8fcd94bf6f0b",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 1.2319941561893075,
  "max_drift_m": 1.2319941561893075,
  "radial_IAE_m_s": 35.143085468790105,
  "signed_longitudinal_delta_m": 1.2317123297896866,
  "tail_speed_mean_m_s": 0.022551296900262426,
  "tail_speed_rms_m_s": 0.022558071945448715,
  "tail_sensor_speed_mean_m_s": 0.02250256396283139,
  "tail_fk_speed_mean_m_s": 0.022503087141161716,
  "peak_tilt_rad": 0.040133637580483716,
  "peak_wheel_torque_nm": 0.11148581653833389,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 11.287288456980605
}
```
