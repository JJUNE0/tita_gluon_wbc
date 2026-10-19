# tita_flash_sac_193248_068255_model_75000_mass130_v02_s913_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 3f7331c3912ccec2acc34ba899d124f69c63f6969c89cf609ed1c0b8f22fcd9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_75000_mass130_v02_s913_300s",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_75000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 913,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "mass": 1.3
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
  "initial_physics_sha256": "701bd77f71bee5d577da8a425d10ede058f59110868551bfa4dc15207176a556",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.10058631499263648,
  "max_drift_m": 0.10280573434537393,
  "radial_IAE_m_s": 20.776364967313942,
  "signed_longitudinal_delta_m": -0.10051475956497413,
  "tail_speed_mean_m_s": -0.00015028067086359192,
  "tail_speed_rms_m_s": 0.0137612489174039,
  "tail_sensor_speed_mean_m_s": 0.001606813783901742,
  "tail_fk_speed_mean_m_s": 0.00010552272671846577,
  "peak_tilt_rad": 0.21821214753888207,
  "peak_wheel_torque_nm": 3.2413642406463623,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.4881420420368634,
  "final_integral_m_s": -0.49802294120176044,
  "elapsed_wall_s": 48.85741894500097
}
```
