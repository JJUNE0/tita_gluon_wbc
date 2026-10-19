# tita_flash_sac_193248_068255_model_95000_friction08_v03_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a9ca81d693e2ee34f29bbb8746ae6c7a09f1a201d1d579d15a861fab83818441

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_95000_friction08_v03_s916",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_95000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "friction": 0.8
    },
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
  "checkpoint_sha256": "a9ca81d693e2ee34f29bbb8746ae6c7a09f1a201d1d579d15a861fab83818441",
  "onnx_sha256": "7e9315ab3ff8de6c69ba7599d9f20f2c432877c181d5c6228d4b55646de7b449",
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
  "initial_physics_sha256": "a29c7986a54e9b26809c834d62e322970d0b254ddd5baffef701167b411ad2cd",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.015105994933578516,
  "max_drift_m": 0.09012868981625662,
  "radial_IAE_m_s": 1.1704492108680706,
  "signed_longitudinal_delta_m": 0.01510456848120026,
  "tail_speed_mean_m_s": -1.7886751012936391e-06,
  "tail_speed_rms_m_s": 3.433210097083161e-05,
  "tail_sensor_speed_mean_m_s": -1.3651228589060785e-06,
  "tail_fk_speed_mean_m_s": -2.0422016266682377e-06,
  "peak_tilt_rad": 0.08581789120808869,
  "peak_wheel_torque_nm": 0.5978821516036987,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.23660105126572473,
  "final_integral_m_s": -0.23660105126572473,
  "elapsed_wall_s": 10.221463529043831
}
```
