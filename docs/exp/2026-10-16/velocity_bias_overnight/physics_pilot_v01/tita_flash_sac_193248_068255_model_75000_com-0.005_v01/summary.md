# tita_flash_sac_193248_068255_model_75000_com-0.005_v01

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 3f7331c3912ccec2acc34ba899d124f69c63f6969c89cf609ed1c0b8f22fcd9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_75000_com-0.005_v01",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_75000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 272,
    "physics": {
      "com": -0.005
    },
    "kick": 0.0,
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.05,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
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
  "initial_physics_sha256": "f374c34a661b66f0899d88aef8cc1f81b17137f70532f09cfeb4080aa2ba95ee",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.03248667658011032,
  "max_drift_m": 0.11957743192570783,
  "radial_IAE_m_s": 1.9936630636493609,
  "signed_longitudinal_delta_m": -0.03248481655347804,
  "tail_speed_mean_m_s": 7.704053985871977e-06,
  "tail_speed_rms_m_s": 7.704497596538128e-06,
  "tail_sensor_speed_mean_m_s": 7.857636658340982e-06,
  "tail_fk_speed_mean_m_s": 7.539270416093546e-06,
  "peak_tilt_rad": 0.15325835607739724,
  "peak_wheel_torque_nm": 2.1067967414855957,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.3558541004322075,
  "final_integral_m_s": -0.3558689590655257,
  "elapsed_wall_s": 5.513499145046808
}
```
