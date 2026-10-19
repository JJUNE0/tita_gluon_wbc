# tita_flash_sac_193248_068255_model_15000_v02_s911_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 04a29ff5621d73fe8056a8ebcd44f66a2477b5d8bc0514955a419f6b336e2081

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_15000_v02_s911_300s",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_15000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 911,
    "estimator": "fk",
    "runtime": true,
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
  "initial_physics_sha256": "4db7e6e6575c907826fbadf8b0c483e35b9ad163d9d10b11bcfa868e2ef07c12",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.019514489375886103,
  "max_drift_m": 0.024635932872724763,
  "radial_IAE_m_s": 5.527405080944801,
  "signed_longitudinal_delta_m": -0.01950718736317171,
  "tail_speed_mean_m_s": -6.751155321348708e-06,
  "tail_speed_rms_m_s": 6.754590743936116e-06,
  "tail_sensor_speed_mean_m_s": -6.254845533415011e-06,
  "tail_fk_speed_mean_m_s": -3.7908399438503427e-06,
  "peak_tilt_rad": 0.09243274105538424,
  "peak_wheel_torque_nm": 0.47343289852142334,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.1922160854679302,
  "final_integral_m_s": -0.19220771798046538,
  "elapsed_wall_s": 55.47341939195758
}
```
