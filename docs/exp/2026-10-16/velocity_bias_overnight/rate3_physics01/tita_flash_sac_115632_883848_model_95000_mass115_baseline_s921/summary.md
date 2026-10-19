# tita_flash_sac_115632_883848_model_95000_mass115_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 7fc976ceb0b69090d3baf26399d36e566e21da7bf1a3f935bf0a1bc7b29a5d82

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_95000_mass115_baseline_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_95000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "mass": 1.15
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
  "initial_physics_sha256": "5ac49c58b610659d64633779d4cd42c54995ca3adc000a95d9becd44ec2413f6",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 10.002522948744208,
  "max_drift_m": 10.002522948744208,
  "radial_IAE_m_s": 300.50809650913794,
  "signed_longitudinal_delta_m": -9.9170726450267,
  "tail_speed_mean_m_s": -0.16591531128072426,
  "tail_speed_rms_m_s": 0.16591690443455565,
  "tail_sensor_speed_mean_m_s": -0.16559497113386146,
  "tail_fk_speed_mean_m_s": -0.16559601759274556,
  "peak_tilt_rad": 0.039396430496661416,
  "peak_wheel_torque_nm": 0.22828823328018188,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 13.747631577949505
}
```
