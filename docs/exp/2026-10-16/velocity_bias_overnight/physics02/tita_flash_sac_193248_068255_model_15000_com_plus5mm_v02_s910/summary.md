# tita_flash_sac_193248_068255_model_15000_com_plus5mm_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 04a29ff5621d73fe8056a8ebcd44f66a2477b5d8bc0514955a419f6b336e2081

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_15000_com_plus5mm_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_15000",
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
  "checkpoint_sha256": "04a29ff5621d73fe8056a8ebcd44f66a2477b5d8bc0514955a419f6b336e2081",
  "onnx_sha256": "2c397ad5d7dbe000ce3559aa35152f7b9a9662e19a7069baff210d46a88a6cb4",
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
  "initial_physics_sha256": "88bbe47dee9a99809ff0409956d8d23f723c4c55c1f8cf65fa757b7d56cc72f5",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.013325769668163717,
  "max_drift_m": 0.01757752469814343,
  "radial_IAE_m_s": 0.7779302068902184,
  "signed_longitudinal_delta_m": -0.01332574797797698,
  "tail_speed_mean_m_s": -1.02313851871497e-05,
  "tail_speed_rms_m_s": 1.0277870699514023e-05,
  "tail_sensor_speed_mean_m_s": -9.91793643259128e-06,
  "tail_fk_speed_mean_m_s": -7.820754238266906e-06,
  "peak_tilt_rad": 0.08298813350019918,
  "peak_wheel_torque_nm": 0.3786129951477051,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.13519204005571514,
  "final_integral_m_s": -0.13518536558979546,
  "elapsed_wall_s": 17.623148885031696
}
```
