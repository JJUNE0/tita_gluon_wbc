# tita_flash_sac_115632_883848_model_85000_friction02_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d1530cc4acd3186dfa88b59087ef850fd51f024ba7eba3252bc14a6549cc77d7

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_85000_friction02_baseline_s916",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_85000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "friction": 0.2
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
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
  "initial_physics_sha256": "75bf454fbd2fc8be10860bcbe5ae833687d71650364f665eba302bf6f498b06a",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 8.373310217874073,
  "max_drift_m": 8.373310217874073,
  "radial_IAE_m_s": 255.2747245624622,
  "signed_longitudinal_delta_m": 8.266994909915159,
  "tail_speed_mean_m_s": 0.1354248111832777,
  "tail_speed_rms_m_s": 0.13542597995800537,
  "tail_sensor_speed_mean_m_s": 0.1351344799951104,
  "tail_fk_speed_mean_m_s": 0.1351350866933203,
  "peak_tilt_rad": 0.06917313882439236,
  "peak_wheel_torque_nm": 0.20363152027130127,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 14.271961623046082
}
```
