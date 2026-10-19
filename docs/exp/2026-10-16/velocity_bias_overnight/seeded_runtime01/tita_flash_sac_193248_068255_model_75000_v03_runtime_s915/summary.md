# tita_flash_sac_193248_068255_model_75000_v03_runtime_s915

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 3f7331c3912ccec2acc34ba899d124f69c63f6969c89cf609ed1c0b8f22fcd9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_75000_v03_runtime_s915",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_75000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 915,
    "estimator": "fk",
    "runtime": true,
    "law": {
      "kp": 0.0,
      "ki": 4.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0,
      "seed_gain": 3.0
    },
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0",
    "controller_source_sha256": "6056e5bd50e0d84e7e554e390f2ede0726c82adf059af80911969c1286a3cded"
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
  "initial_physics_sha256": "8e8046981a574ab352941d865b6d45c3590e0c11dc9944705981fcafc354268c",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.006934894555989636,
  "max_drift_m": 0.055170032481259075,
  "radial_IAE_m_s": 0.5503512514418116,
  "signed_longitudinal_delta_m": -0.006917201773889027,
  "tail_speed_mean_m_s": 2.8782759266645446e-05,
  "tail_speed_rms_m_s": 2.8785066961569725e-05,
  "tail_sensor_speed_mean_m_s": 2.8854008267695185e-05,
  "tail_fk_speed_mean_m_s": 2.8439684117184787e-05,
  "peak_tilt_rad": 0.08417938635446998,
  "peak_wheel_torque_nm": 0.4477745294570923,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.27698545227480453,
  "final_integral_m_s": -0.27698545227480453,
  "elapsed_wall_s": 16.8831142319832
}
```
