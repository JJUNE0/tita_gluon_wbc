# tita_flash_sac_193248_068255_model_75000_com_plus5mm_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 3f7331c3912ccec2acc34ba899d124f69c63f6969c89cf609ed1c0b8f22fcd9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_75000_com_plus5mm_baseline_s916",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_75000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "com": 0.005
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
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
  "initial_physics_sha256": "f22f5aa43a37303f131ccc49c2d09cf7788521eb3de6be85271a3c684b0fa0fc",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 8.268477566006645,
  "max_drift_m": 8.268477566006645,
  "radial_IAE_m_s": 226.5045930813177,
  "signed_longitudinal_delta_m": -8.05541335159525,
  "tail_speed_mean_m_s": -0.16599297951749045,
  "tail_speed_rms_m_s": 0.16637633275641855,
  "tail_sensor_speed_mean_m_s": -0.16578025164865431,
  "tail_fk_speed_mean_m_s": -0.16578573294668666,
  "peak_tilt_rad": 0.05352925939138253,
  "peak_wheel_torque_nm": 0.3003411889076233,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 12.752038748993073
}
```
