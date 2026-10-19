# tita_flash_sac_193248_068255_model_5000_kick+0.2_v02_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 0c6ce2fc849b775f8b54d68c5d62b070104e18f4036bbfa1d259bf96543c3f65

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_5000_kick+0.2_v02_s912",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_5000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 912,
    "estimator": "fk",
    "runtime": true,
    "kick": 0.2,
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
  "initial_physics_sha256": "fc51b69994523b93c375155c9ce3aaee2cdc4dfa543419dc2bfb1e67b27dab4f",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.09860661878169028,
  "max_drift_m": 0.09972161273554414,
  "radial_IAE_m_s": 5.766908488440796,
  "signed_longitudinal_delta_m": -0.09857557161535034,
  "tail_speed_mean_m_s": 2.1236709067319232e-05,
  "tail_speed_rms_m_s": 2.1243282515777905e-05,
  "tail_sensor_speed_mean_m_s": 1.6791557132307406e-05,
  "tail_fk_speed_mean_m_s": 1.1228918685931598e-05,
  "peak_tilt_rad": 0.10302609177955424,
  "peak_wheel_torque_nm": 4.643779754638672,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -1.0194419611208965,
  "final_integral_m_s": -1.0194644313413714,
  "elapsed_wall_s": 15.645613770000637
}
```
