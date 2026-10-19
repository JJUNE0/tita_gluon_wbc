# tita_flash_sac_193248_068255_model_15000_tau0.05_entry12

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 04a29ff5621d73fe8056a8ebcd44f66a2477b5d8bc0514955a419f6b336e2081

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_15000_tau0.05_entry12",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_15000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 271,
    "estimator": "fk",
    "runtime": true,
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.05,
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
  "initial_physics_sha256": "57114fdbdd982bdafdabd489efe7aea8de5335cdb8f2da51e2540164d91520f9",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.017806106862127836,
  "max_drift_m": 0.02332288075110343,
  "radial_IAE_m_s": 1.055363875984873,
  "signed_longitudinal_delta_m": -0.0178042664139153,
  "tail_speed_mean_m_s": -5.730263592788107e-06,
  "tail_speed_rms_m_s": 5.732375093314422e-06,
  "tail_sensor_speed_mean_m_s": -5.894159557236777e-06,
  "tail_fk_speed_mean_m_s": -3.5806236771726303e-06,
  "peak_tilt_rad": 0.09022606378805853,
  "peak_wheel_torque_nm": 0.5612058639526367,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.1825249388066554,
  "final_integral_m_s": -0.18251761679599104,
  "elapsed_wall_s": 5.917280266992748
}
```
