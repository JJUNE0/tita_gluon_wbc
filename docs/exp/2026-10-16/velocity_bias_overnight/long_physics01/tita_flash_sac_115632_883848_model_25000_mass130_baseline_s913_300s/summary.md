# tita_flash_sac_115632_883848_model_25000_mass130_baseline_s913_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: fd99df31c9e160baa980cd421917f4536bfda16779ad79754dd3d4bf13c600b1

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_25000_mass130_baseline_s913_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_25000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 913,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "mass": 1.3
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "fd99df31c9e160baa980cd421917f4536bfda16779ad79754dd3d4bf13c600b1",
  "onnx_sha256": "494320c9b871a706a00e8f350ff196243c37e61c0d12ed2ab0503ea24d273b8f",
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
  "initial_physics_sha256": "be384ae0ef3bd35b41cd172cd0ba416f1642415acda235b4869d322689089b10",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 27.139687613082742,
  "max_drift_m": 27.139687613082742,
  "radial_IAE_m_s": 4101.5249756393205,
  "signed_longitudinal_delta_m": 26.016750071261775,
  "tail_speed_mean_m_s": 0.0916779603721064,
  "tail_speed_rms_m_s": 0.09167796037485279,
  "tail_sensor_speed_mean_m_s": 0.09148095567293532,
  "tail_fk_speed_mean_m_s": 0.09147895053639328,
  "peak_tilt_rad": 0.11973059494486926,
  "peak_wheel_torque_nm": 1.2776062488555908,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 39.965240819961764
}
```
