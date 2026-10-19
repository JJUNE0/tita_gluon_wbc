# tita_flash_sac_193248_068255_model_60000_kick+0.2_v03_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 9b0d8897472dc567619d49df3e6df08813dcbb15b018f23ed58060e92e1b139b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_60000_kick+0.2_v03_s917",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_60000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 917,
    "estimator": "fk",
    "guarded": true,
    "kick": 0.2,
    "law": {
      "kp": 0.0,
      "ki": 4.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0,
      "seed_gain": 3.0
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
  "final_drift_m": 0.00583350969964474,
  "max_drift_m": 0.09900487924842334,
  "radial_IAE_m_s": 0.3884225752834935,
  "signed_longitudinal_delta_m": 0.005833457004067449,
  "tail_speed_mean_m_s": 8.797484357750823e-05,
  "tail_speed_rms_m_s": 8.798221611723645e-05,
  "tail_sensor_speed_mean_m_s": 8.753692740469725e-05,
  "tail_fk_speed_mean_m_s": 8.976171968671399e-05,
  "peak_tilt_rad": 0.07157488251736477,
  "peak_wheel_torque_nm": 1.4767193794250488,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.011348333643863773,
  "final_integral_m_s": -0.011348333643863773,
  "elapsed_wall_s": 12.401067694008816
}
```
