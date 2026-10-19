# tita_flash_sac_193248_068255_model_60000_com_plus5mm_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 9b0d8897472dc567619d49df3e6df08813dcbb15b018f23ed58060e92e1b139b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_60000_com_plus5mm_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_60000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "com": 0.005
    },
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
  "initial_physics_sha256": "595d36f087c11ee78f25fa6d2fcd4c25e7464d9eb80cfe9334a08d9318683d41",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.007212043516666511,
  "max_drift_m": 0.0074005933682053686,
  "radial_IAE_m_s": 0.3927516438040147,
  "signed_longitudinal_delta_m": 0.0072117014030593065,
  "tail_speed_mean_m_s": 1.884114227789427e-05,
  "tail_speed_rms_m_s": 1.9706135951655523e-05,
  "tail_sensor_speed_mean_m_s": 1.8442849578490387e-05,
  "tail_fk_speed_mean_m_s": 2.094847373477781e-05,
  "peak_tilt_rad": 0.03831270179456636,
  "peak_wheel_torque_nm": 0.14010746777057648,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.07532996655092503,
  "final_integral_m_s": 0.07529807901307344,
  "elapsed_wall_s": 17.204373461019713
}
```
