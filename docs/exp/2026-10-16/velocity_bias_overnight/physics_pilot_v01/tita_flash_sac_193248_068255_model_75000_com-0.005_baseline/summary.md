# tita_flash_sac_193248_068255_model_75000_com-0.005_baseline

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 3f7331c3912ccec2acc34ba899d124f69c63f6969c89cf609ed1c0b8f22fcd9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_75000_com-0.005_baseline",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_75000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 272,
    "physics": {
      "com": -0.005
    },
    "kick": 0.0,
    "law": {
      "mode": "constant",
      "bias": 0.0
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
  "initial_physics_sha256": "f374c34a661b66f0899d88aef8cc1f81b17137f70532f09cfeb4080aa2ba95ee",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 14.885595238562853,
  "max_drift_m": 14.885595238562853,
  "radial_IAE_m_s": 456.6484935290923,
  "signed_longitudinal_delta_m": -11.41241261905677,
  "tail_speed_mean_m_s": -0.30281042973536776,
  "tail_speed_rms_m_s": 0.3028570442483203,
  "tail_sensor_speed_mean_m_s": -0.30243783971055166,
  "tail_fk_speed_mean_m_s": -0.30247637939135497,
  "peak_tilt_rad": 0.015227547730359614,
  "peak_wheel_torque_nm": 0.10613405704498291,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 5.372238223964814
}
```
