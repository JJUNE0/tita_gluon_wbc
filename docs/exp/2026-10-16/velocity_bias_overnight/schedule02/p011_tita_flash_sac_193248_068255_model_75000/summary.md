# p011_tita_flash_sac_193248_068255_model_75000

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 3f7331c3912ccec2acc34ba899d124f69c63f6969c89cf609ed1c0b8f22fcd9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "p011_tita_flash_sac_193248_068255_model_75000",
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
      "gain_velocity": 0.1,
      "gain_tau": 1.0,
      "gain_floor": 0.25
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
  "final_drift_m": 0.00506237700740152,
  "max_drift_m": 0.10272499887283584,
  "radial_IAE_m_s": 0.5156930205025528,
  "signed_longitudinal_delta_m": 0.004961035749294882,
  "tail_speed_mean_m_s": -3.3381780895584914e-05,
  "tail_speed_rms_m_s": 0.005028856893629364,
  "tail_sensor_speed_mean_m_s": 0.00011512847666746898,
  "tail_fk_speed_mean_m_s": 1.9304846940360604e-05,
  "peak_tilt_rad": 0.2182121203158096,
  "peak_wheel_torque_nm": 2.411395788192749,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.5032426557369752,
  "final_integral_m_s": -0.5042321508983975,
  "elapsed_wall_s": 12.037849259970244
}
```
