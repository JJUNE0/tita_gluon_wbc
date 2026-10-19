# tita_flash_sac_115632_883848_model_90000_kick+0.2_baseline_s922

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 4930085834f72c133d65563169762514342959361a6d71630216f5f608b0531f

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_90000_kick+0.2_baseline_s922",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_90000",
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
  "checkpoint_sha256": "4930085834f72c133d65563169762514342959361a6d71630216f5f608b0531f",
  "onnx_sha256": "1d6ffa5d91a15cf74e2abf755c367c1fb151f6e3c740618a6e1fb2fbf28f9379",
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
  "initial_physics_sha256": "bc5ac01e5d84fc2106e771481df32bcd28ad357efbd9f8501e4fab2bf3fb6cfc",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 6.860410083035991,
  "max_drift_m": 6.860410083035991,
  "radial_IAE_m_s": 208.64761008757648,
  "signed_longitudinal_delta_m": 6.858932531404885,
  "tail_speed_mean_m_s": 0.11340309727319275,
  "tail_speed_rms_m_s": 0.11340333821906333,
  "tail_sensor_speed_mean_m_s": 0.11315765914305816,
  "tail_fk_speed_mean_m_s": 0.11315589866353128,
  "peak_tilt_rad": 0.08517131868681638,
  "peak_wheel_torque_nm": 1.7361873388290405,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 5.129114130977541
}
```
