# tita_flash_sac_115632_883848_model_95000_kick+0.2_baseline_s922

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 7fc976ceb0b69090d3baf26399d36e566e21da7bf1a3f935bf0a1bc7b29a5d82

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_95000_kick+0.2_baseline_s922",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_95000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 922,
    "estimator": "fk",
    "guarded": false,
    "kick": 0.2,
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
  },
  "checkpoint_sha256": "7fc976ceb0b69090d3baf26399d36e566e21da7bf1a3f935bf0a1bc7b29a5d82",
  "onnx_sha256": "1a45e6567675d4dfc1a738bbe430e52a4f2a2cab73c2c908c46928d22bd54530",
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
  "initial_physics_sha256": "b5ff1c49c2cec8e9eb0b6a08e266bc08c03eb7ce7862755e68273a4c01e436de",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 1.405188598619688,
  "max_drift_m": 1.405188598619688,
  "radial_IAE_m_s": 42.74072291173856,
  "signed_longitudinal_delta_m": 1.4042506518752684,
  "tail_speed_mean_m_s": 0.025702118188742115,
  "tail_speed_rms_m_s": 0.02573947716859698,
  "tail_sensor_speed_mean_m_s": 0.025646991262363965,
  "tail_fk_speed_mean_m_s": 0.025646942361228563,
  "peak_tilt_rad": 0.0822858401318538,
  "peak_wheel_torque_nm": 1.8451200723648071,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 5.189072948007379
}
```
