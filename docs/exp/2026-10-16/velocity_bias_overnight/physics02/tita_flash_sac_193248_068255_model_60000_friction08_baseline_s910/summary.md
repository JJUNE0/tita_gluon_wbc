# tita_flash_sac_193248_068255_model_60000_friction08_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 9b0d8897472dc567619d49df3e6df08813dcbb15b018f23ed58060e92e1b139b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_60000_friction08_baseline_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_60000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "friction": 0.8
    },
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
  "initial_physics_sha256": "227eb80d004d4fcdab7011f135ba30b4010055f8df6abc14489c3f25e5c1a0e9",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.478701941173983,
  "max_drift_m": 0.478701941173983,
  "radial_IAE_m_s": 16.30272459608592,
  "signed_longitudinal_delta_m": -0.47817794131957503,
  "tail_speed_mean_m_s": -0.00592073168301283,
  "tail_speed_rms_m_s": 0.005945938505262386,
  "tail_sensor_speed_mean_m_s": -0.005907982869404471,
  "tail_fk_speed_mean_m_s": -0.0059056444803383965,
  "peak_tilt_rad": 0.03376099053339865,
  "peak_wheel_torque_nm": 0.09774170815944672,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 13.566811099997722
}
```
