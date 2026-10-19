# tita_flash_sac_193248_068255_model_75000_kick-0.2_baseline_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 3f7331c3912ccec2acc34ba899d124f69c63f6969c89cf609ed1c0b8f22fcd9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_75000_kick-0.2_baseline_s912",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_75000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 912,
    "estimator": "fk",
    "runtime": false,
    "kick": -0.2,
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
  "initial_physics_sha256": "17f9956a4a6373f65b4c6e719c999351fbec27284b0abbbdecacd94cbc40feaa",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 13.107493349776336,
  "max_drift_m": 13.107493349776336,
  "radial_IAE_m_s": 392.9128155942782,
  "signed_longitudinal_delta_m": -11.349404706825915,
  "tail_speed_mean_m_s": -0.2559136389264889,
  "tail_speed_rms_m_s": 0.2559941244061162,
  "tail_sensor_speed_mean_m_s": -0.25561375736783737,
  "tail_fk_speed_mean_m_s": -0.2556414299074054,
  "peak_tilt_rad": 0.04830134387753415,
  "peak_wheel_torque_nm": 1.6109483242034912,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.046659165003803
}
```
