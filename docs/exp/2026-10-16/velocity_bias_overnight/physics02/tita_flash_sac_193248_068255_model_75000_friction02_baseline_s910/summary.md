# tita_flash_sac_193248_068255_model_75000_friction02_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 3f7331c3912ccec2acc34ba899d124f69c63f6969c89cf609ed1c0b8f22fcd9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_75000_friction02_baseline_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_75000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "friction": 0.2
    },
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
  "initial_physics_sha256": "da33364e10601b9b63a17b4872ca40816c545319d744b33fdd8c38cae4947857",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 5.58700168100566,
  "max_drift_m": 5.58700168100566,
  "radial_IAE_m_s": 172.20163779772537,
  "signed_longitudinal_delta_m": -5.52317648109885,
  "tail_speed_mean_m_s": -0.08789158457848704,
  "tail_speed_rms_m_s": 0.08790540150016317,
  "tail_sensor_speed_mean_m_s": -0.08777463545838982,
  "tail_fk_speed_mean_m_s": -0.087776510066277,
  "peak_tilt_rad": 0.05010772319591705,
  "peak_wheel_torque_nm": 0.29273056983947754,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 11.899524519045372
}
```
