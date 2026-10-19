# tita_flash_sac_115632_883848_model_95000_kick-0.2_baseline_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 7fc976ceb0b69090d3baf26399d36e566e21da7bf1a3f935bf0a1bc7b29a5d82

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_95000_kick-0.2_baseline_s912",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_95000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 912,
    "estimator": "fk",
    "runtime": false,
    "kick": -0.2,
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
  "initial_physics_sha256": "408bb601abda4270c007aaee7b68440239b73bfff8e9996e7cb94a3c9f1b3330",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.8093782362282259,
  "max_drift_m": 0.8093782362282259,
  "radial_IAE_m_s": 17.21002321278785,
  "signed_longitudinal_delta_m": 0.8080454295061671,
  "tail_speed_mean_m_s": 0.024130445009796914,
  "tail_speed_rms_m_s": 0.02417804437621762,
  "tail_sensor_speed_mean_m_s": 0.024078726059396677,
  "tail_fk_speed_mean_m_s": 0.024078679113365645,
  "peak_tilt_rad": 0.06440385363305778,
  "peak_wheel_torque_nm": 1.6321773529052734,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 17.680269179982133
}
```
