# tita_flash_sac_193248_068255_model_5000_mass115_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 0c6ce2fc849b775f8b54d68c5d62b070104e18f4036bbfa1d259bf96543c3f65

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_5000_mass115_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_5000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "mass": 1.15
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
  "checkpoint_sha256": "0c6ce2fc849b775f8b54d68c5d62b070104e18f4036bbfa1d259bf96543c3f65",
  "onnx_sha256": "0db9e18936f3f631b4beff658e5d721600ad74d65fe6401c55ff3c8c9fa7b2ea",
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
  "initial_physics_sha256": "842cdbd61c227c1e25246bc270fddb36533603ad8e4b5f728ecdf18b62acce5c",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.10921455027854542,
  "max_drift_m": 0.11047871889205775,
  "radial_IAE_m_s": 6.466133111166034,
  "signed_longitudinal_delta_m": -0.10918205374668456,
  "tail_speed_mean_m_s": 2.499099486355682e-05,
  "tail_speed_rms_m_s": 2.499341565414493e-05,
  "tail_sensor_speed_mean_m_s": 9.475352769368206e-06,
  "tail_fk_speed_mean_m_s": -3.7107350665541934e-07,
  "peak_tilt_rad": 0.09388197340327986,
  "peak_wheel_torque_nm": 1.6664602756500244,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -1.116519438936062,
  "final_integral_m_s": -1.1165192447798085,
  "elapsed_wall_s": 11.770857592986431
}
```
