# tita_flash_sac_193248_068255_model_5000_v03_s918_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 0c6ce2fc849b775f8b54d68c5d62b070104e18f4036bbfa1d259bf96543c3f65

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_5000_v03_s918_300s",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_5000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 918,
    "estimator": "fk",
    "guarded": true,
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
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
  },
  "checkpoint_sha256": "0c6ce2fc849b775f8b54d68c5d62b070104e18f4036bbfa1d259bf96543c3f65",
  "onnx_sha256": "0db9e18936f3f631b4beff658e5d721600ad74d65fe6401c55ff3c8c9fa7b2ea",
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
  "initial_physics_sha256": "b60b192b9d2f23858fdffe55ec465d178806e473ef4c4913e439a7ef2e3a0fd4",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.19801798514861188,
  "max_drift_m": 0.20383778623002313,
  "radial_IAE_m_s": 59.444797175055996,
  "signed_longitudinal_delta_m": -0.19800526731222137,
  "tail_speed_mean_m_s": 1.2421185674786371e-05,
  "tail_speed_rms_m_s": 1.2421846081693213e-05,
  "tail_sensor_speed_mean_m_s": 1.2790906113585039e-05,
  "tail_fk_speed_mean_m_s": 8.589796553399214e-06,
  "peak_tilt_rad": 0.07525703404705664,
  "peak_wheel_torque_nm": 0.9056854844093323,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -1.0001505463681926,
  "final_integral_m_s": -1.0001505463681926,
  "elapsed_wall_s": 45.041086763027124
}
```
