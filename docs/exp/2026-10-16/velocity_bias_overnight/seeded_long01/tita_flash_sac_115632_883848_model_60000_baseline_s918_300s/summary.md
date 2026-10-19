# tita_flash_sac_115632_883848_model_60000_baseline_s918_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_60000_baseline_s918_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_60000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 918,
    "estimator": "fk",
    "guarded": false,
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
  },
  "checkpoint_sha256": "6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05",
  "onnx_sha256": "f44f07ed44970e3ff565eae67fd9229adf0be5c02215591c52a691ffcbb71b2a",
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
  "initial_physics_sha256": "eb56f0041445c657351c1c0fd66d0dab00823a96a3d588a19c1708de1d21159d",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 5.323403807507411,
  "max_drift_m": 5.323403807507411,
  "radial_IAE_m_s": 762.4701942746594,
  "signed_longitudinal_delta_m": 5.248891089579862,
  "tail_speed_mean_m_s": 0.019472988472015944,
  "tail_speed_rms_m_s": 0.019473007351810085,
  "tail_sensor_speed_mean_m_s": 0.019430404335964598,
  "tail_fk_speed_mean_m_s": 0.01943170869002274,
  "peak_tilt_rad": 0.06993139895410172,
  "peak_wheel_torque_nm": 0.15149882435798645,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 44.01855425600661
}
```
