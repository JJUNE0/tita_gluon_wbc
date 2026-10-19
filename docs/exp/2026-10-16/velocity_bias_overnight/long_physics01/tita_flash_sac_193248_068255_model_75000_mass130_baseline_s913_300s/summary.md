# tita_flash_sac_193248_068255_model_75000_mass130_baseline_s913_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 3f7331c3912ccec2acc34ba899d124f69c63f6969c89cf609ed1c0b8f22fcd9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_75000_mass130_baseline_s913_300s",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_75000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 913,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "mass": 1.3
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
  "initial_physics_sha256": "701bd77f71bee5d577da8a425d10ede058f59110868551bfa4dc15207176a556",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 16.7839731121897,
  "max_drift_m": 17.103055167838438,
  "radial_IAE_m_s": 4479.114961158895,
  "signed_longitudinal_delta_m": -14.451189063246964,
  "tail_speed_mean_m_s": -0.0095851008959834,
  "tail_speed_rms_m_s": 0.00958510104012998,
  "tail_sensor_speed_mean_m_s": -0.009488533647713984,
  "tail_fk_speed_mean_m_s": -0.00942447128893021,
  "peak_tilt_rad": 0.13910232977331627,
  "peak_wheel_torque_nm": 0.6799317002296448,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 28.332443912979215
}
```
