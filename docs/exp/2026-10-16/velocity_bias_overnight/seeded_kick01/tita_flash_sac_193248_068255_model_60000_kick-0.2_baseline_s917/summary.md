# tita_flash_sac_193248_068255_model_60000_kick-0.2_baseline_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 9b0d8897472dc567619d49df3e6df08813dcbb15b018f23ed58060e92e1b139b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_60000_kick-0.2_baseline_s917",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_60000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 917,
    "estimator": "fk",
    "guarded": false,
    "kick": -0.2,
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
  "initial_physics_sha256": "e98eb756d782b88a72670889a79aafbb9339fade78f14535bd5ff2c64b7058f7",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.5197021310777478,
  "max_drift_m": 0.5197021310777478,
  "radial_IAE_m_s": 22.394513160958425,
  "signed_longitudinal_delta_m": -0.5195316352113295,
  "tail_speed_mean_m_s": -0.003894983242709659,
  "tail_speed_rms_m_s": 0.003928438167477489,
  "tail_sensor_speed_mean_m_s": -0.0038864596793179,
  "tail_fk_speed_mean_m_s": -0.0038843582671573076,
  "peak_tilt_rad": 0.03408419015622699,
  "peak_wheel_torque_nm": 1.495036005973816,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 11.186345829046331
}
```
