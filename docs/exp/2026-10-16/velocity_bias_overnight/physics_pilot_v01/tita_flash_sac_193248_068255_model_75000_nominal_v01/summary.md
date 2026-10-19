# tita_flash_sac_193248_068255_model_75000_nominal_v01

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 3f7331c3912ccec2acc34ba899d124f69c63f6969c89cf609ed1c0b8f22fcd9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_75000_nominal_v01",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_75000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 272,
    "physics": {},
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
  "initial_physics_sha256": "fbc5df3efdc8ffb7939436a546f14b0be6b79b66d55f9ffcac9b0c65b6911729",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.025614927802023717,
  "max_drift_m": 0.09525441521284558,
  "radial_IAE_m_s": 1.5861499625892033,
  "signed_longitudinal_delta_m": -0.025613679085481043,
  "tail_speed_mean_m_s": 1.4282773497365356e-05,
  "tail_speed_rms_m_s": 1.4283595992352098e-05,
  "tail_sensor_speed_mean_m_s": 1.4468240848801346e-05,
  "tail_fk_speed_mean_m_s": 1.3997545030201167e-05,
  "peak_tilt_rad": 0.1269349654399381,
  "peak_wheel_torque_nm": 1.6359139680862427,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.28280252875257,
  "final_integral_m_s": -0.28283012168014715,
  "elapsed_wall_s": 4.700431239034515
}
```
