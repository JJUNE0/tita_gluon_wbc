# tita_flash_sac_193248_068255_model_5000_s271

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 0c6ce2fc849b775f8b54d68c5d62b070104e18f4036bbfa1d259bf96543c3f65

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_5000_s271",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_5000",
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
  "initial_physics_sha256": "5b72cdc663a8f0b30c38d6d96cc7eb00379427f44a92f7d5e1ca5df0cf2f54c5",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.0993103245738849,
  "max_drift_m": 0.10028471383717623,
  "radial_IAE_m_s": 5.8211206487714175,
  "signed_longitudinal_delta_m": -0.09914179244326995,
  "tail_speed_mean_m_s": 1.7309417736860636e-05,
  "tail_speed_rms_m_s": 1.7325920355417238e-05,
  "tail_sensor_speed_mean_m_s": 1.480887572957093e-05,
  "tail_fk_speed_mean_m_s": 9.831208762309768e-06,
  "peak_tilt_rad": 0.07890792005349012,
  "peak_wheel_torque_nm": 0.6912032961845398,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -1.0097096297291581,
  "final_integral_m_s": -1.0097279421772396,
  "elapsed_wall_s": 4.458417257992551
}
```
