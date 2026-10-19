# tita_flash_sac_193248_068255_model_75000_tau0.1_entry12

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 3f7331c3912ccec2acc34ba899d124f69c63f6969c89cf609ed1c0b8f22fcd9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_75000_tau0.1_entry12",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_75000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 271,
    "estimator": "fk",
    "runtime": true,
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
  "initial_physics_sha256": "edbecdcabcb3b5b1727f169a584e77bd3c57aba7e643861f796a585ba0e61e2c",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.02697099147224918,
  "max_drift_m": 0.04746307211274863,
  "radial_IAE_m_s": 1.644863934078003,
  "signed_longitudinal_delta_m": -0.02696832983535415,
  "tail_speed_mean_m_s": 1.3060198712039174e-05,
  "tail_speed_rms_m_s": 1.3080412782667353e-05,
  "tail_sensor_speed_mean_m_s": 1.321153325348185e-05,
  "tail_fk_speed_mean_m_s": 1.2766630833242983e-05,
  "peak_tilt_rad": 0.08461679311743153,
  "peak_wheel_torque_nm": 0.4291251003742218,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.2802514668902875,
  "final_integral_m_s": -0.28027514153063826,
  "elapsed_wall_s": 18.950195881014224
}
```
