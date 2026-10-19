# tita_flash_sac_193248_068255_model_5000_kick+0.2_baseline_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 0c6ce2fc849b775f8b54d68c5d62b070104e18f4036bbfa1d259bf96543c3f65

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_5000_kick+0.2_baseline_s912",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_5000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 912,
    "estimator": "fk",
    "runtime": false,
    "kick": 0.2,
    "law": {
      "mode": "constant",
      "bias": 0.0
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
  "final_drift_m": 1.4837297115864336,
  "max_drift_m": 1.6215169396540532,
  "radial_IAE_m_s": 67.77412905487412,
  "signed_longitudinal_delta_m": -0.11326478070733179,
  "tail_speed_mean_m_s": -0.04462612184567189,
  "tail_speed_rms_m_s": 0.044638487342268385,
  "tail_sensor_speed_mean_m_s": -0.04523037964226615,
  "tail_fk_speed_mean_m_s": -0.045591507238366955,
  "peak_tilt_rad": 0.08896261305775122,
  "peak_wheel_torque_nm": 4.642054080963135,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 10.129100502992515
}
```
