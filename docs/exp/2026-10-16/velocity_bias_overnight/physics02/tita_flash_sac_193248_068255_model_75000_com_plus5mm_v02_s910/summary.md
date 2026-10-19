# tita_flash_sac_193248_068255_model_75000_com_plus5mm_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 3f7331c3912ccec2acc34ba899d124f69c63f6969c89cf609ed1c0b8f22fcd9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_75000_com_plus5mm_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_75000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "com": 0.005
    },
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
  "initial_physics_sha256": "d0a1e55654f6f905a86004ad0c543a2da9878252f66835c4b88e279eefcce5e5",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.01890156567533627,
  "max_drift_m": 0.03368469152968889,
  "radial_IAE_m_s": 1.1665361208635558,
  "signed_longitudinal_delta_m": -0.018901337794259787,
  "tail_speed_mean_m_s": 1.6733345557206886e-05,
  "tail_speed_rms_m_s": 1.673427587528342e-05,
  "tail_sensor_speed_mean_m_s": 1.695217951957337e-05,
  "tail_fk_speed_mean_m_s": 1.6370212995253925e-05,
  "peak_tilt_rad": 0.0722095232643798,
  "peak_wheel_torque_nm": 0.4721393585205078,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.19547716996978198,
  "final_integral_m_s": -0.1955093267190659,
  "elapsed_wall_s": 17.29447802499635
}
```
