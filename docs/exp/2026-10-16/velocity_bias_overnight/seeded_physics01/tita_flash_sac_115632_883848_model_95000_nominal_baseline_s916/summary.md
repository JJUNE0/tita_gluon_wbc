# tita_flash_sac_115632_883848_model_95000_nominal_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 7fc976ceb0b69090d3baf26399d36e566e21da7bf1a3f935bf0a1bc7b29a5d82

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_95000_nominal_baseline_s916",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_95000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": false,
    "physics": {},
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
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
  "initial_physics_sha256": "5225adb92b861b6f386707359cfb90ab85f90e1ef27be7a8d2c9dba79df4b891",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 1.096182609474644,
  "max_drift_m": 1.096182609474644,
  "radial_IAE_m_s": 27.159939825167264,
  "signed_longitudinal_delta_m": 1.0954636696844708,
  "tail_speed_mean_m_s": 0.024270457330770604,
  "tail_speed_rms_m_s": 0.02431770370569905,
  "tail_sensor_speed_mean_m_s": 0.024218459435729776,
  "tail_fk_speed_mean_m_s": 0.024218388417107103,
  "peak_tilt_rad": 0.06442296075758924,
  "peak_wheel_torque_nm": 0.1854180544614792,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 14.147736107988749
}
```
