# tita_flash_sac_193248_068255_model_75000_nominal_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 3f7331c3912ccec2acc34ba899d124f69c63f6969c89cf609ed1c0b8f22fcd9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_75000_nominal_baseline_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_75000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {},
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
  "initial_physics_sha256": "538e3ebb0ac86a7b3a658515a654845c84cea5519fd72111666245b20a00a053",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 12.825922011528364,
  "max_drift_m": 12.825922011528364,
  "radial_IAE_m_s": 374.9827577941084,
  "signed_longitudinal_delta_m": -11.221270196432233,
  "tail_speed_mean_m_s": -0.25394161805192766,
  "tail_speed_rms_m_s": 0.25403004103855376,
  "tail_sensor_speed_mean_m_s": -0.2536468897849916,
  "tail_fk_speed_mean_m_s": -0.25367315509383576,
  "peak_tilt_rad": 0.04835152066521031,
  "peak_wheel_torque_nm": 0.29201510548591614,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 11.711696601007134
}
```
