# tita_flash_sac_115632_883848_model_95000_friction02_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 7fc976ceb0b69090d3baf26399d36e566e21da7bf1a3f935bf0a1bc7b29a5d82

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_95000_friction02_baseline_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_95000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "friction": 0.2
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "7fc976ceb0b69090d3baf26399d36e566e21da7bf1a3f935bf0a1bc7b29a5d82",
  "onnx_sha256": "1a45e6567675d4dfc1a738bbe430e52a4f2a2cab73c2c908c46928d22bd54530",
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
  "initial_physics_sha256": "17e65aea4c83f5580e319d5c88e3e57140d4fb2d0d0b258ea2cff5a3d600026e",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 3.2700597452986546,
  "max_drift_m": 3.2700597452986546,
  "radial_IAE_m_s": 101.9589903358099,
  "signed_longitudinal_delta_m": 2.9676738586601488,
  "tail_speed_mean_m_s": 0.052523394738217606,
  "tail_speed_rms_m_s": 0.05252446546748334,
  "tail_sensor_speed_mean_m_s": 0.05243976087554789,
  "tail_fk_speed_mean_m_s": 0.05244251909475903,
  "peak_tilt_rad": 0.06787879910199712,
  "peak_wheel_torque_nm": 0.249202698469162,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 11.470898765022866
}
```
