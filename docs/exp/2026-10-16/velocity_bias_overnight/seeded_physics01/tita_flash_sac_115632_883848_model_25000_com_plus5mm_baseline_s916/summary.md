# tita_flash_sac_115632_883848_model_25000_com_plus5mm_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: fd99df31c9e160baa980cd421917f4536bfda16779ad79754dd3d4bf13c600b1

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_25000_com_plus5mm_baseline_s916",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_25000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "com": 0.005
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
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
  "initial_physics_sha256": "ee5d8dc4cb51fdb951e90638b88b9688160a893a49bdbc3f0c2a352fd232fa5a",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 22.75322549919166,
  "max_drift_m": 22.75322549919166,
  "radial_IAE_m_s": 687.761608924391,
  "signed_longitudinal_delta_m": 22.08587928707323,
  "tail_speed_mean_m_s": 0.38544728190918986,
  "tail_speed_rms_m_s": 0.3854472819098718,
  "tail_sensor_speed_mean_m_s": 0.3846393909212567,
  "tail_fk_speed_mean_m_s": 0.3846186027841854,
  "peak_tilt_rad": 0.14206355274932614,
  "peak_wheel_torque_nm": 1.4067264795303345,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 16.15401214902522
}
```
