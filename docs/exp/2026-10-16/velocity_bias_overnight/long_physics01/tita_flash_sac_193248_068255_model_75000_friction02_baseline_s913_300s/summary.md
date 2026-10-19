# tita_flash_sac_193248_068255_model_75000_friction02_baseline_s913_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 3f7331c3912ccec2acc34ba899d124f69c63f6969c89cf609ed1c0b8f22fcd9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_75000_friction02_baseline_s913_300s",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_75000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 913,
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
  "initial_physics_sha256": "af54ac61e0fe8f1b230567f1966a84ce99d73c238dd1c2cf652b7558de8f09d5",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 7.14106921632356,
  "max_drift_m": 11.709370486938878,
  "radial_IAE_m_s": 2499.2967165456616,
  "signed_longitudinal_delta_m": -3.5959605464218565,
  "tail_speed_mean_m_s": -0.052135099209796885,
  "tail_speed_rms_m_s": 0.0521405679215132,
  "tail_sensor_speed_mean_m_s": -0.052062038285094654,
  "tail_fk_speed_mean_m_s": -0.05207339638318547,
  "peak_tilt_rad": 0.050107738607591434,
  "peak_wheel_torque_nm": 0.29273587465286255,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 26.9390029089991
}
```
