# tita_flash_sac_115632_883848_model_95000_kick+0.2_baseline_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 7fc976ceb0b69090d3baf26399d36e566e21da7bf1a3f935bf0a1bc7b29a5d82

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_95000_kick+0.2_baseline_s912",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_95000",
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
  "initial_physics_sha256": "976ca1dfde724286a72e580d701206ad55b6d6c0a7e09e41aea85814f251eaef",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 1.405190775219508,
  "max_drift_m": 1.405190775219508,
  "radial_IAE_m_s": 42.74079622428938,
  "signed_longitudinal_delta_m": 1.4042528284473934,
  "tail_speed_mean_m_s": 0.02570214648127965,
  "tail_speed_rms_m_s": 0.02573950432237408,
  "tail_sensor_speed_mean_m_s": 0.025647019117632175,
  "tail_fk_speed_mean_m_s": 0.025646970293555223,
  "peak_tilt_rad": 0.08228583392920896,
  "peak_wheel_torque_nm": 1.8451212644577026,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 14.962040109036025
}
```
