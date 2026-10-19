# tita_flash_sac_193248_068255_model_75000_nominal_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 3f7331c3912ccec2acc34ba899d124f69c63f6969c89cf609ed1c0b8f22fcd9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_75000_nominal_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_75000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {},
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
  "initial_physics_sha256": "538e3ebb0ac86a7b3a658515a654845c84cea5519fd72111666245b20a00a053",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.026921462399589004,
  "max_drift_m": 0.04729895165004386,
  "radial_IAE_m_s": 1.6414359562210348,
  "signed_longitudinal_delta_m": -0.02691876268956242,
  "tail_speed_mean_m_s": 1.263969031290916e-05,
  "tail_speed_rms_m_s": 1.2657302958433859e-05,
  "tail_sensor_speed_mean_m_s": 1.2783454247178e-05,
  "tail_fk_speed_mean_m_s": 1.234558120531688e-05,
  "peak_tilt_rad": 0.08442238638826272,
  "peak_wheel_torque_nm": 0.4329511523246765,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.27970332049369395,
  "final_integral_m_s": -0.2797267288845661,
  "elapsed_wall_s": 16.100011224974878
}
```
