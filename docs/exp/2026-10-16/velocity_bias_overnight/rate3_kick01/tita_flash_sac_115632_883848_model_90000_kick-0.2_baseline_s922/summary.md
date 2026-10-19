# tita_flash_sac_115632_883848_model_90000_kick-0.2_baseline_s922

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 4930085834f72c133d65563169762514342959361a6d71630216f5f608b0531f

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_90000_kick-0.2_baseline_s922",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_90000",
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
  "initial_physics_sha256": "a775b4f11caeb259f53b633f2a8d888f8448434305c4c226f6dde4f778f502bf",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 6.503233549331113,
  "max_drift_m": 6.503233549331113,
  "radial_IAE_m_s": 187.80474726920025,
  "signed_longitudinal_delta_m": 6.501293061326308,
  "tail_speed_mean_m_s": 0.11329873097382837,
  "tail_speed_rms_m_s": 0.1132990117410626,
  "tail_sensor_speed_mean_m_s": 0.1130534638177823,
  "tail_fk_speed_mean_m_s": 0.11305176107002238,
  "peak_tilt_rad": 0.0704531499458354,
  "peak_wheel_torque_nm": 1.87337327003479,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 7.761575804965105
}
```
