# tita_flash_sac_193248_068255_model_5000_v02_s911_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 0c6ce2fc849b775f8b54d68c5d62b070104e18f4036bbfa1d259bf96543c3f65

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_5000_v02_s911_300s",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_5000",
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
  "initial_physics_sha256": "3777e810fa1deaca1eb648c4968d7987aee33398d3c11d60ee5f6763a3bf1aae",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.09771225527496569,
  "max_drift_m": 0.10099870862501556,
  "radial_IAE_m_s": 29.51565057349868,
  "signed_longitudinal_delta_m": -0.09770879165894042,
  "tail_speed_mean_m_s": 7.240706745572369e-06,
  "tail_speed_rms_m_s": 7.241073812956777e-06,
  "tail_sensor_speed_mean_m_s": 7.615588720650782e-06,
  "tail_fk_speed_mean_m_s": 3.4187290993385885e-06,
  "peak_tilt_rad": 0.0752376784059261,
  "peak_wheel_torque_nm": 0.9531166553497314,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.9999908182090437,
  "final_integral_m_s": -0.9999974263871654,
  "elapsed_wall_s": 74.31090689398116
}
```
