# tita_flash_sac_193248_068255_model_60000_kick+0.2_baseline_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 9b0d8897472dc567619d49df3e6df08813dcbb15b018f23ed58060e92e1b139b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_60000_kick+0.2_baseline_s917",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_60000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 917,
    "estimator": "fk",
    "guarded": false,
    "kick": 0.2,
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
  "initial_physics_sha256": "0b9a1923be0772f24f4d846ab4e0ce6c054deb58c383af9f78ce5b4618673d5e",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.13639201716555338,
  "max_drift_m": 0.1564433357235585,
  "radial_IAE_m_s": 4.7168987834626765,
  "signed_longitudinal_delta_m": -0.1358255425597164,
  "tail_speed_mean_m_s": -0.003511949427959164,
  "tail_speed_rms_m_s": 0.003548898878390698,
  "tail_sensor_speed_mean_m_s": -0.0035042014975479284,
  "tail_fk_speed_mean_m_s": -0.003502169296298,
  "peak_tilt_rad": 0.07169822340257559,
  "peak_wheel_torque_nm": 1.4836444854736328,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 11.638595152006019
}
```
