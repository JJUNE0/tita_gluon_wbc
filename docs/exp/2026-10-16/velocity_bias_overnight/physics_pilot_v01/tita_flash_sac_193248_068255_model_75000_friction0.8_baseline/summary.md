# tita_flash_sac_193248_068255_model_75000_friction0.8_baseline

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 3f7331c3912ccec2acc34ba899d124f69c63f6969c89cf609ed1c0b8f22fcd9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_75000_friction0.8_baseline",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_75000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 272,
    "physics": {
      "friction": 0.8
    },
    "kick": 0.0,
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "estimator": "fk"
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
  "initial_physics_sha256": "8546bce7186455c967bf35be62d5644bc544b00ff3c85502b32ff7fb696a0977",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 13.289172909106066,
  "max_drift_m": 13.289172909106066,
  "radial_IAE_m_s": 414.5983501879295,
  "signed_longitudinal_delta_m": -9.12293071517875,
  "tail_speed_mean_m_s": -0.2783365329747203,
  "tail_speed_rms_m_s": 0.27841348517667547,
  "tail_sensor_speed_mean_m_s": -0.2779323721677127,
  "tail_fk_speed_mean_m_s": -0.2779801021307149,
  "peak_tilt_rad": 0.020512559058270208,
  "peak_wheel_torque_nm": 0.10275721549987793,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 5.340905577992089
}
```
