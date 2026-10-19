# tita_flash_sac_193248_068255_model_75000_mass115_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 3f7331c3912ccec2acc34ba899d124f69c63f6969c89cf609ed1c0b8f22fcd9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_75000_mass115_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_75000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "mass": 1.15
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
  "initial_physics_sha256": "b08a0747dc4734b4631bd5c2fab8c754c1bb9984707334fcca73bb60aa188434",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.0420594746631796,
  "max_drift_m": 0.0760454404802615,
  "radial_IAE_m_s": 2.5311455838993955,
  "signed_longitudinal_delta_m": -0.04205691837418001,
  "tail_speed_mean_m_s": 2.2763283843162145e-06,
  "tail_speed_rms_m_s": 2.2767627654847386e-06,
  "tail_sensor_speed_mean_m_s": 2.2788588637244366e-06,
  "tail_fk_speed_mean_m_s": 1.7760678460830485e-06,
  "peak_tilt_rad": 0.1430291011563214,
  "peak_wheel_torque_nm": 1.529528021812439,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.4399378965166511,
  "final_integral_m_s": -0.4399413677756111,
  "elapsed_wall_s": 19.83750829100609
}
```
