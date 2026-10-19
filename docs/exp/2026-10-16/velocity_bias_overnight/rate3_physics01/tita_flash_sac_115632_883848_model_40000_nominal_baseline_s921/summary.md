# tita_flash_sac_115632_883848_model_40000_nominal_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a4b5c15c3add7114e65d55cabbe505c0fffcd993df1b9162587e073cca97a891

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_40000_nominal_baseline_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_40000",
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
  "checkpoint_sha256": "a4b5c15c3add7114e65d55cabbe505c0fffcd993df1b9162587e073cca97a891",
  "onnx_sha256": "4722a7e5dc4a1d465689d98943ba5c9a40a7d45a99344f923f067d1cfa90fcb6",
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
  "initial_physics_sha256": "3dda3dd72b78fc981d9b4aa4ddc1fcfbf54a72d586703e4b6abc0f4ce0c03d1f",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 7.0838776152727085,
  "max_drift_m": 7.0838776152727085,
  "radial_IAE_m_s": 212.3760688736049,
  "signed_longitudinal_delta_m": 7.066904436759878,
  "tail_speed_mean_m_s": 0.1177107417790427,
  "tail_speed_rms_m_s": 0.1177111322142309,
  "tail_sensor_speed_mean_m_s": 0.11745616170900079,
  "tail_fk_speed_mean_m_s": 0.11745645661297713,
  "peak_tilt_rad": 0.11578624265544035,
  "peak_wheel_torque_nm": 0.31667542457580566,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.986133138008881
}
```
