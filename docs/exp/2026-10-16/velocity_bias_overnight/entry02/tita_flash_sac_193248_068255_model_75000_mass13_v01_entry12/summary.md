# tita_flash_sac_193248_068255_model_75000_mass13_v01_entry12

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 3f7331c3912ccec2acc34ba899d124f69c63f6969c89cf609ed1c0b8f22fcd9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_75000_mass13_v01_entry12",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_75000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 272,
    "estimator": "fk",
    "physics": {
      "mass": 1.3
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
  "initial_physics_sha256": "8edf6f231ad43616ea4705b6e570f184822947870b98818f820fd0eef693dbd8",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.0785351272439594,
  "max_drift_m": 0.1004509978506375,
  "radial_IAE_m_s": 3.7567369058834696,
  "signed_longitudinal_delta_m": -0.07839170236060085,
  "tail_speed_mean_m_s": -0.0004708080983514182,
  "tail_speed_rms_m_s": 0.022662609303024623,
  "tail_sensor_speed_mean_m_s": 0.0013926911709266187,
  "tail_fk_speed_mean_m_s": 1.5993351763631835e-05,
  "peak_tilt_rad": 0.21346522734003726,
  "peak_wheel_torque_nm": 5.351591110229492,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.5441653325498715,
  "final_integral_m_s": -0.4828276430329739,
  "elapsed_wall_s": 5.4410436999751255
}
```
