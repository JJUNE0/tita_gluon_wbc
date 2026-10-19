# tita_flash_sac_115632_883848_model_25000_nominal_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: fd99df31c9e160baa980cd421917f4536bfda16779ad79754dd3d4bf13c600b1

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_25000_nominal_v04_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_25000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": true,
    "physics": {},
    "law": {
      "kp": 0.0,
      "ki": 4.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 3.0,
      "seed_gain": 3.0
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
  "initial_physics_sha256": "4ad5099153fe1627dbed4177e18a5fa695fef94243db292b7595f4c2016f98da",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.09189218054794779,
  "max_drift_m": 0.17139103134091552,
  "radial_IAE_m_s": 4.87291042299747,
  "signed_longitudinal_delta_m": 0.09189213439947298,
  "tail_speed_mean_m_s": 0.00038980239468613243,
  "tail_speed_rms_m_s": 0.00039274990162896584,
  "tail_sensor_speed_mean_m_s": 0.00038914123618147614,
  "tail_fk_speed_mean_m_s": 0.000398584871304654,
  "peak_tilt_rad": 0.13909894913135012,
  "peak_wheel_torque_nm": 2.0482006072998047,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 1.3382559795313185,
  "final_integral_m_s": 1.3382559795313185,
  "elapsed_wall_s": 9.914385851996485
}
```
