# tita_flash_sac_193248_068255_model_75000_friction0.2_v01

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 3f7331c3912ccec2acc34ba899d124f69c63f6969c89cf609ed1c0b8f22fcd9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_75000_friction0.2_v01",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_75000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 272,
    "physics": {
      "friction": 0.2
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
  "initial_physics_sha256": "6bfe1757a54c308d85586f25a600212bdcc9c69a754b959c7288507dc333f266",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.021842458824305105,
  "max_drift_m": 0.045267934799979224,
  "radial_IAE_m_s": 1.3218181495771955,
  "signed_longitudinal_delta_m": -0.021841586093034496,
  "tail_speed_mean_m_s": -1.197287754756597e-06,
  "tail_speed_rms_m_s": 1.1978878728081857e-06,
  "tail_sensor_speed_mean_m_s": -1.2083644094533243e-06,
  "tail_fk_speed_mean_m_s": -1.4069408200346679e-06,
  "peak_tilt_rad": 0.07956088645564541,
  "peak_wheel_torque_nm": 0.5771957635879517,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.23169991512277102,
  "final_integral_m_s": -0.2316971807191804,
  "elapsed_wall_s": 5.326070887967944
}
```
