# tita_flash_sac_115632_883848_model_95000_friction02_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 7fc976ceb0b69090d3baf26399d36e566e21da7bf1a3f935bf0a1bc7b29a5d82

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_95000_friction02_baseline_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_95000",
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
  "initial_physics_sha256": "f399c2c095634ca40da9f58723c9fe3beb1df467323b3f05e9a001be13494557",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 3.270059943747015,
  "max_drift_m": 3.270059943747015,
  "radial_IAE_m_s": 101.95899504833397,
  "signed_longitudinal_delta_m": 2.9676739449285052,
  "tail_speed_mean_m_s": 0.052523398286710286,
  "tail_speed_rms_m_s": 0.05252446913576783,
  "tail_sensor_speed_mean_m_s": 0.0524397642369917,
  "tail_fk_speed_mean_m_s": 0.05244252265000025,
  "peak_tilt_rad": 0.06787880466365959,
  "peak_wheel_torque_nm": 0.2492041438817978,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 13.68287653598236
}
```
