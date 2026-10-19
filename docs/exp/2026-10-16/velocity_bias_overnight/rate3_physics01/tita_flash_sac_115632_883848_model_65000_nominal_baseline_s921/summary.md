# tita_flash_sac_115632_883848_model_65000_nominal_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a28e8551929d9a4412f571a2e91577da75879477c15d61f0774ab6f05354dff3

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_65000_nominal_baseline_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_65000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": false,
    "physics": {},
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
  },
  "checkpoint_sha256": "a28e8551929d9a4412f571a2e91577da75879477c15d61f0774ab6f05354dff3",
  "onnx_sha256": "7cc289e8aee44513f1e29487c7522e96c762174e2444aedaa7aea78b3a66a3ec",
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
  "initial_physics_sha256": "c2607dac168f2bbe35d201b5347e7f78d83271aca9242e2d49d84bc25807e196",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 1.9968037415912392,
  "max_drift_m": 1.9968037415912392,
  "radial_IAE_m_s": 60.98846613084524,
  "signed_longitudinal_delta_m": 1.9889668555843671,
  "tail_speed_mean_m_s": 0.03200861999958929,
  "tail_speed_rms_m_s": 0.03201227527769367,
  "tail_sensor_speed_mean_m_s": 0.03193934630835676,
  "tail_fk_speed_mean_m_s": 0.03193816911616808,
  "peak_tilt_rad": 0.059626760689986735,
  "peak_wheel_torque_nm": 0.25075483322143555,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 8.303170589031652
}
```
