# tita_flash_sac_115632_883848_model_25000_mass130_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: fd99df31c9e160baa980cd421917f4536bfda16779ad79754dd3d4bf13c600b1

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_25000_mass130_baseline_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_25000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "mass": 1.3
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
  },
  "checkpoint_sha256": "fd99df31c9e160baa980cd421917f4536bfda16779ad79754dd3d4bf13c600b1",
  "onnx_sha256": "494320c9b871a706a00e8f350ff196243c37e61c0d12ed2ab0503ea24d273b8f",
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
  "initial_physics_sha256": "083776cb89d4bef68bd64bf4494f2c6e9771cae452ac215c3021388656f93aa8",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 5.512372174271381,
  "max_drift_m": 5.512372174271381,
  "radial_IAE_m_s": 165.21315648437675,
  "signed_longitudinal_delta_m": 5.503271825802915,
  "tail_speed_mean_m_s": 0.09193542781432139,
  "tail_speed_rms_m_s": 0.0919354432684509,
  "tail_sensor_speed_mean_m_s": 0.09173794479039711,
  "tail_fk_speed_mean_m_s": 0.09173587747215697,
  "peak_tilt_rad": 0.11973062168165005,
  "peak_wheel_torque_nm": 1.277601957321167,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.822948695975356
}
```
