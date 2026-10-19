# tita_flash_sac_193248_068255_model_75000_nominal_fk

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 3f7331c3912ccec2acc34ba899d124f69c63f6969c89cf609ed1c0b8f22fcd9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_75000_nominal_fk",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_75000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 272,
    "estimator": "fk",
    "physics": {},
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
  "initial_physics_sha256": "fbc5df3efdc8ffb7939436a546f14b0be6b79b66d55f9ffcac9b0c65b6911729",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.02558383225483668,
  "max_drift_m": 0.09732457310424619,
  "radial_IAE_m_s": 1.587786484774122,
  "signed_longitudinal_delta_m": -0.025581712875002875,
  "tail_speed_mean_m_s": 1.4244265166385974e-05,
  "tail_speed_rms_m_s": 1.4245089153358475e-05,
  "tail_sensor_speed_mean_m_s": 1.4430831954441012e-05,
  "tail_fk_speed_mean_m_s": 1.3957838197275057e-05,
  "peak_tilt_rad": 0.13176020636077568,
  "peak_wheel_torque_nm": 1.579740047454834,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.2825954162606418,
  "final_integral_m_s": -0.2826228626029625,
  "elapsed_wall_s": 13.035085986019112
}
```
