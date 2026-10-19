# tita_flash_sac_115632_883848_model_25000_kick-0.2_baseline_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: fd99df31c9e160baa980cd421917f4536bfda16779ad79754dd3d4bf13c600b1

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_25000_kick-0.2_baseline_s917",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_25000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 917,
    "estimator": "fk",
    "guarded": false,
    "kick": -0.2,
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
  "initial_physics_sha256": "eb5f3687019017a742c82823f57c28b9568eedb2ec54b69c358dd1adcc57147e",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 21.94253256765077,
  "max_drift_m": 21.94253256765077,
  "radial_IAE_m_s": 660.6928571858939,
  "signed_longitudinal_delta_m": 21.339933677663353,
  "tail_speed_mean_m_s": 0.3736960319699916,
  "tail_speed_rms_m_s": 0.3737053589747077,
  "tail_sensor_speed_mean_m_s": 0.3729184340723154,
  "tail_fk_speed_mean_m_s": 0.3728985531789882,
  "peak_tilt_rad": 0.14352694425612778,
  "peak_wheel_torque_nm": 1.9554498195648193,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 11.058198095008265
}
```
