# tita_flash_sac_115632_883848_model_85000_friction02_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d1530cc4acd3186dfa88b59087ef850fd51f024ba7eba3252bc14a6549cc77d7

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_85000_friction02_baseline_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_85000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "friction": 0.2
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
  },
  "checkpoint_sha256": "d1530cc4acd3186dfa88b59087ef850fd51f024ba7eba3252bc14a6549cc77d7",
  "onnx_sha256": "1ed320e4785fe0edd047b9aa7e4185e975602f208fcf3deca0a9aa486c76114c",
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
  "initial_physics_sha256": "cad1f6e990ae010256f9113175b8eb583d34fc0219eb70c6217f995a4adcbed8",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 8.37330980540392,
  "max_drift_m": 8.37330980540392,
  "radial_IAE_m_s": 255.2747089758769,
  "signed_longitudinal_delta_m": 8.266994641608802,
  "tail_speed_mean_m_s": 0.1354248057957546,
  "tail_speed_rms_m_s": 0.13542597453749802,
  "tail_sensor_speed_mean_m_s": 0.13513447472071102,
  "tail_fk_speed_mean_m_s": 0.13513508155209264,
  "peak_tilt_rad": 0.06917314476180203,
  "peak_wheel_torque_nm": 0.20363390445709229,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 10.778555202996358
}
```
