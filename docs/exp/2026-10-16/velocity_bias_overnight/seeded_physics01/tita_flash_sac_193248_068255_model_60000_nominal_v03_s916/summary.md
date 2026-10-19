# tita_flash_sac_193248_068255_model_60000_nominal_v03_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 9b0d8897472dc567619d49df3e6df08813dcbb15b018f23ed58060e92e1b139b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_60000_nominal_v03_s916",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_60000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": true,
    "physics": {},
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
  "initial_physics_sha256": "31edf6aeb73c950842406c8f6d237b5649c95bd946d39fa1916fbeef58af209d",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.004359511313041258,
  "max_drift_m": 0.005423160270040759,
  "radial_IAE_m_s": 0.12173748423365222,
  "signed_longitudinal_delta_m": 0.004325047417862317,
  "tail_speed_mean_m_s": 8.875392099305818e-05,
  "tail_speed_rms_m_s": 8.876084238351171e-05,
  "tail_sensor_speed_mean_m_s": 8.82759188859449e-05,
  "tail_fk_speed_mean_m_s": 9.051537994095802e-05,
  "peak_tilt_rad": 0.03942522224079892,
  "peak_wheel_torque_nm": 0.14056949317455292,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.012766141732535643,
  "final_integral_m_s": -0.012766141732535643,
  "elapsed_wall_s": 10.83833770401543
}
```
