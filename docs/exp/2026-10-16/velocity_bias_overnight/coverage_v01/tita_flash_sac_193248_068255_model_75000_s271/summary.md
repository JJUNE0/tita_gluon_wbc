# tita_flash_sac_193248_068255_model_75000_s271

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 3f7331c3912ccec2acc34ba899d124f69c63f6969c89cf609ed1c0b8f22fcd9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_75000_s271",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_75000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 271,
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
  "initial_physics_sha256": "6b2ec49e7940edc5bf31b1df1514327db976e85d0bb544cea4cc1112130ce352",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.025614917211287287,
  "max_drift_m": 0.09525441718154273,
  "radial_IAE_m_s": 1.586149983395281,
  "signed_longitudinal_delta_m": -0.025613668510438604,
  "tail_speed_mean_m_s": 1.4282540138058497e-05,
  "tail_speed_rms_m_s": 1.4283321149586547e-05,
  "tail_sensor_speed_mean_m_s": 1.4468468127909672e-05,
  "tail_fk_speed_mean_m_s": 1.3996870521067636e-05,
  "peak_tilt_rad": 0.12693496184170838,
  "peak_wheel_torque_nm": 1.6359131336212158,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.2828025487442754,
  "final_integral_m_s": -0.2828299948968127,
  "elapsed_wall_s": 4.420258502999786
}
```
