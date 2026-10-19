# tita_flash_sac_115632_883848_model_95000_com_minus5mm_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 7fc976ceb0b69090d3baf26399d36e566e21da7bf1a3f935bf0a1bc7b29a5d82

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_95000_com_minus5mm_baseline_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_95000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "com": -0.005
    },
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
  "initial_physics_sha256": "e0e07f2968cd233dd361ae011f279f6a4a6a5b47e9f965503217f667c91fc4be",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.8230014091003631,
  "max_drift_m": 0.8230014091003631,
  "radial_IAE_m_s": 28.687429928006985,
  "signed_longitudinal_delta_m": -0.8225890455851135,
  "tail_speed_mean_m_s": -0.009433222959048528,
  "tail_speed_rms_m_s": 0.009526487201262987,
  "tail_sensor_speed_mean_m_s": -0.009412549607895903,
  "tail_fk_speed_mean_m_s": -0.009412477499055188,
  "peak_tilt_rad": 0.05723955698712602,
  "peak_wheel_torque_nm": 0.15498793125152588,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 13.614775165973697
}
```
