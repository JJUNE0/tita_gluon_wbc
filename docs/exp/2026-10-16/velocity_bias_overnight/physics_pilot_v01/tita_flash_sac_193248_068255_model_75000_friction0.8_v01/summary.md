# tita_flash_sac_193248_068255_model_75000_friction0.8_v01

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 3f7331c3912ccec2acc34ba899d124f69c63f6969c89cf609ed1c0b8f22fcd9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_75000_friction0.8_v01",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_75000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 272,
    "physics": {
      "friction": 0.8
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
  "initial_physics_sha256": "8546bce7186455c967bf35be62d5644bc544b00ff3c85502b32ff7fb696a0977",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.02645083699620021,
  "max_drift_m": 0.10392787334085372,
  "radial_IAE_m_s": 1.6435503311388842,
  "signed_longitudinal_delta_m": -0.02644983655937475,
  "tail_speed_mean_m_s": 1.6212230012859172e-05,
  "tail_speed_rms_m_s": 1.6213077641290775e-05,
  "tail_sensor_speed_mean_m_s": 1.652062433698738e-05,
  "tail_fk_speed_mean_m_s": 1.599274752767627e-05,
  "peak_tilt_rad": 0.13637326209503442,
  "peak_wheel_torque_nm": 1.8369030952453613,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.2930731870876782,
  "final_integral_m_s": -0.293104601226908,
  "elapsed_wall_s": 5.430901466985233
}
```
