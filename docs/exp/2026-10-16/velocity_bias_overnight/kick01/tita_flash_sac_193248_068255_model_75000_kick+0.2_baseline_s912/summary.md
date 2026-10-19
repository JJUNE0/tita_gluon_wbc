# tita_flash_sac_193248_068255_model_75000_kick+0.2_baseline_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 3f7331c3912ccec2acc34ba899d124f69c63f6969c89cf609ed1c0b8f22fcd9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_75000_kick+0.2_baseline_s912",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_75000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 912,
    "estimator": "fk",
    "runtime": false,
    "kick": 0.2,
    "law": {
      "mode": "constant",
      "bias": 0.0
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
  "initial_physics_sha256": "53b56c604513738923dcbc55088e1385758193149616a5b11749e35fc65bcb05",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 12.459859146278987,
  "max_drift_m": 12.459859146278987,
  "radial_IAE_m_s": 352.37056185297325,
  "signed_longitudinal_delta_m": -10.997940997722463,
  "tail_speed_mean_m_s": -0.2518548440107199,
  "tail_speed_rms_m_s": 0.2519515315632714,
  "tail_sensor_speed_mean_m_s": -0.25156272004439584,
  "tail_fk_speed_mean_m_s": -0.25158883298358414,
  "peak_tilt_rad": 0.06838000324172477,
  "peak_wheel_torque_nm": 1.6726690530776978,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 8.496605149994139
}
```
