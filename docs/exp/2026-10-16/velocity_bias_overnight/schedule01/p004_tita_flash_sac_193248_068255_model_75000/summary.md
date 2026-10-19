# p004_tita_flash_sac_193248_068255_model_75000

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 3f7331c3912ccec2acc34ba899d124f69c63f6969c89cf609ed1c0b8f22fcd9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "p004_tita_flash_sac_193248_068255_model_75000",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_75000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
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
      "slew": 2.0,
      "gain_velocity": 0.05,
      "gain_floor": 0.1
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
  "initial_physics_sha256": "39084eea07633b0d2cc199570bbfd541a6d57a61ec6ff767086ffeda1bce9d1c",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.05126519826631578,
  "max_drift_m": 0.10276625973370203,
  "radial_IAE_m_s": 3.0459929241229218,
  "signed_longitudinal_delta_m": -0.051243787306313876,
  "tail_speed_mean_m_s": -1.0103176572158866e-05,
  "tail_speed_rms_m_s": 0.004618378065478588,
  "tail_sensor_speed_mean_m_s": 0.00020353322683732284,
  "tail_fk_speed_mean_m_s": -2.4287206052137558e-06,
  "peak_tilt_rad": 0.21742289673088822,
  "peak_wheel_torque_nm": 2.5253803730010986,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.5033964609463033,
  "final_integral_m_s": -0.5039183596253295,
  "elapsed_wall_s": 14.261206188006327
}
```
