# tita_flash_sac_193248_068255_model_5000_v03_runtime_s915

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 0c6ce2fc849b775f8b54d68c5d62b070104e18f4036bbfa1d259bf96543c3f65

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_5000_v03_runtime_s915",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_5000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 915,
    "estimator": "fk",
    "runtime": true,
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
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0",
    "controller_source_sha256": "6056e5bd50e0d84e7e554e390f2ede0726c82adf059af80911969c1286a3cded"
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
  "initial_physics_sha256": "484bf81443fddad9d00ceedf10c942b74f301a835707c7b0c13fec9351747b7a",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.20081628711629093,
  "max_drift_m": 0.2024163726391667,
  "radial_IAE_m_s": 11.49757109017991,
  "signed_longitudinal_delta_m": -0.20077768604037693,
  "tail_speed_mean_m_s": 3.616490865771846e-05,
  "tail_speed_rms_m_s": 3.620615439803361e-05,
  "tail_sensor_speed_mean_m_s": 3.269464390403164e-05,
  "tail_fk_speed_mean_m_s": 2.7435270009027392e-05,
  "peak_tilt_rad": 0.07525370296968936,
  "peak_wheel_torque_nm": 0.8683120012283325,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -1.0112610245143479,
  "final_integral_m_s": -1.0112610245143479,
  "elapsed_wall_s": 16.80610127199907
}
```
