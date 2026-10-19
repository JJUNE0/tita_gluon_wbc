# p001_tita_flash_sac_193248_068255_model_75000

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 3f7331c3912ccec2acc34ba899d124f69c63f6969c89cf609ed1c0b8f22fcd9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "p001_tita_flash_sac_193248_068255_model_75000",
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
      "ki": 1.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0,
      "seed_gain": 2.0
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
  "final_drift_m": 0.12187902936852939,
  "max_drift_m": 0.1997605974834095,
  "radial_IAE_m_s": 7.408938695478177,
  "signed_longitudinal_delta_m": -0.12186920519499404,
  "tail_speed_mean_m_s": -3.09371206354245e-05,
  "tail_speed_rms_m_s": 0.004331933042267583,
  "tail_sensor_speed_mean_m_s": -0.00020427298244849804,
  "tail_fk_speed_mean_m_s": -3.270436314422355e-05,
  "peak_tilt_rad": 0.15204397965700744,
  "peak_wheel_torque_nm": 1.8934063911437988,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.5044604069621981,
  "final_integral_m_s": -0.5044604069621981,
  "elapsed_wall_s": 5.230932151956949
}
```
