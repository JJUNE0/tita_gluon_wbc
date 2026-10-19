# tita_flash_sac_193248_068255_model_75000_friction02_v01_entry12

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 3f7331c3912ccec2acc34ba899d124f69c63f6969c89cf609ed1c0b8f22fcd9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_75000_friction02_v01_entry12",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_75000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 272,
    "estimator": "fk",
    "physics": {
      "friction": 0.2
    },
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.05,
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
  "initial_physics_sha256": "b3808cb76e0ff9506c4d2a18b90ae110e93a771458f24298891fa301b83323e9",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.022704882109601796,
  "max_drift_m": 0.032485584182016095,
  "radial_IAE_m_s": 1.3633318787558701,
  "signed_longitudinal_delta_m": -0.022702742445217243,
  "tail_speed_mean_m_s": -7.750083087800727e-07,
  "tail_speed_rms_m_s": 7.759198446029603e-07,
  "tail_sensor_speed_mean_m_s": -7.92916271490619e-07,
  "tail_fk_speed_mean_m_s": -9.969813939507616e-07,
  "peak_tilt_rad": 0.07035408446804814,
  "peak_wheel_torque_nm": 0.5274639129638672,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.2336526699533598,
  "final_integral_m_s": -0.23365095579037648,
  "elapsed_wall_s": 5.2130306489998475
}
```
