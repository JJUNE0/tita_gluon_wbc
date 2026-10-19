# tita_flash_sac_115632_883848_model_75000_kick-0.2_baseline_s922

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 381e846e3ffb1d5a9ed629c02b55c9740ec3c5b089ca443f38b3d73b6abbd730

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_75000_kick-0.2_baseline_s922",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_75000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 922,
    "estimator": "fk",
    "guarded": false,
    "kick": -0.2,
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
  },
  "checkpoint_sha256": "381e846e3ffb1d5a9ed629c02b55c9740ec3c5b089ca443f38b3d73b6abbd730",
  "onnx_sha256": "2bd3f78d10bc3b7cc4e50272d0289147f13b0a62ac6730048ba653ae53f35114",
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
  "initial_physics_sha256": "c6c9b3d4cea365fa328498c811e553172cc0fca051bf471d31299ca09569c6b6",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.2695730564493378,
  "max_drift_m": 0.3028657997756722,
  "radial_IAE_m_s": 17.31878541799207,
  "signed_longitudinal_delta_m": -0.2695659335448078,
  "tail_speed_mean_m_s": 0.0011453461198645432,
  "tail_speed_rms_m_s": 0.0011611413699237243,
  "tail_sensor_speed_mean_m_s": 0.0011429645153342766,
  "tail_fk_speed_mean_m_s": 0.0011434721836160418,
  "peak_tilt_rad": 0.051923125924935754,
  "peak_wheel_torque_nm": 1.6450133323669434,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 8.717533472983632
}
```
