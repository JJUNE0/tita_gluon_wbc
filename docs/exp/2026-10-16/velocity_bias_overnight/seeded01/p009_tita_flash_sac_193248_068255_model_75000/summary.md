# p009_tita_flash_sac_193248_068255_model_75000

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 3f7331c3912ccec2acc34ba899d124f69c63f6969c89cf609ed1c0b8f22fcd9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "p009_tita_flash_sac_193248_068255_model_75000",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_75000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "physics": {
      "mass": 1.3
    },
    "kick": 0.0,
    "law": {
      "kp": 0.0,
      "ki": 0.5,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0,
      "seed_gain": 5.0
    }
  },
  "checkpoint_sha256": "3f7331c3912ccec2acc34ba899d124f69c63f6969c89cf609ed1c0b8f22fcd9a",
  "onnx_sha256": "ba89df992b5d2cb9fbeaff0a274ee0d50d022a90cd2982cdd88750a3adf35d15",
  "input_columns": [
    "velocity_bias_m_s",
    "filtered_velocity_m_s",
    "integral_m_s"
  ],
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
  "final_drift_m": 0.9017954850670751,
  "max_drift_m": 0.9306163636584035,
  "radial_IAE_m_s": 51.49730914073093,
  "signed_longitudinal_delta_m": 0.9016139643493579,
  "tail_speed_mean_m_s": -1.5666496933704305e-05,
  "tail_speed_rms_m_s": 0.00452521010087435,
  "tail_sensor_speed_mean_m_s": -0.00011874649284659892,
  "tail_fk_speed_mean_m_s": -2.7242254363897212e-05,
  "peak_tilt_rad": 0.21815061367794408,
  "peak_wheel_torque_nm": 1.9174301624298096,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.5043091095972183,
  "final_integral_m_s": -0.5043091095972183,
  "elapsed_wall_s": 5.374491063004825
}
```
