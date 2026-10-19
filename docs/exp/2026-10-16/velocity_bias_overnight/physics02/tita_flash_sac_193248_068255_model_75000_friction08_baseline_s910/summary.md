# tita_flash_sac_193248_068255_model_75000_friction08_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 3f7331c3912ccec2acc34ba899d124f69c63f6969c89cf609ed1c0b8f22fcd9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_75000_friction08_baseline_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_75000",
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
  "checkpoint_sha256": "3f7331c3912ccec2acc34ba899d124f69c63f6969c89cf609ed1c0b8f22fcd9a",
  "onnx_sha256": "ba89df992b5d2cb9fbeaff0a274ee0d50d022a90cd2982cdd88750a3adf35d15",
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
  "initial_physics_sha256": "c66e3a96bbb1148b4de54d6fe917757ee088adc354242e632857ad84d25bdf3a",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 13.076520676188924,
  "max_drift_m": 13.076520676188924,
  "radial_IAE_m_s": 395.8676008844657,
  "signed_longitudinal_delta_m": -9.878084751431919,
  "tail_speed_mean_m_s": -0.2704562613669397,
  "tail_speed_rms_m_s": 0.2705178623017035,
  "tail_sensor_speed_mean_m_s": -0.27008863791343285,
  "tail_fk_speed_mean_m_s": -0.270134826704576,
  "peak_tilt_rad": 0.047630264069692174,
  "peak_wheel_torque_nm": 0.2872416377067566,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 12.95649814902572
}
```
