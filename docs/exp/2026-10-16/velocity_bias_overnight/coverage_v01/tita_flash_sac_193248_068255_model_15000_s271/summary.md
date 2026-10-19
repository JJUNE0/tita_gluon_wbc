# tita_flash_sac_193248_068255_model_15000_s271

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 04a29ff5621d73fe8056a8ebcd44f66a2477b5d8bc0514955a419f6b336e2081

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_15000_s271",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_15000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 271,
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.05,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
    },
    "estimator": "fk"
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
  "initial_physics_sha256": "7d80e5aaa7facbf7f87d6a3c3f94551361f57e7e25ddc93b3bb6e1e0a5df0688",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.01782833824655264,
  "max_drift_m": 0.02327121358561726,
  "radial_IAE_m_s": 1.0557938474764499,
  "signed_longitudinal_delta_m": -0.01782530842063801,
  "tail_speed_mean_m_s": -5.830779962303133e-06,
  "tail_speed_rms_m_s": 5.83905340351076e-06,
  "tail_sensor_speed_mean_m_s": -5.889259848027201e-06,
  "tail_fk_speed_mean_m_s": -3.5762598229625938e-06,
  "peak_tilt_rad": 0.09011341314014132,
  "peak_wheel_torque_nm": 0.5770347714424133,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.1824274761427412,
  "final_integral_m_s": -0.1824200493403434,
  "elapsed_wall_s": 4.406785532017238
}
```
