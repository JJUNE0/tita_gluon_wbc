# tita_flash_sac_115632_883848_model_25000_friction02_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: fd99df31c9e160baa980cd421917f4536bfda16779ad79754dd3d4bf13c600b1

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_25000_friction02_baseline_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_25000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "friction": 0.2
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
  "initial_physics_sha256": "71f7f327c2f3328bddb7be07e835383f7054ebe5c17e7db0bbe2020fbb42611f",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.08780090901828608,
  "max_drift_m": 0.08796298761686416,
  "radial_IAE_m_s": 2.5064739285183,
  "signed_longitudinal_delta_m": -0.08771315737442738,
  "tail_speed_mean_m_s": -0.001506112266987483,
  "tail_speed_rms_m_s": 0.007948049502648264,
  "tail_sensor_speed_mean_m_s": 7.9784078220277745,
  "tail_fk_speed_mean_m_s": 7.978361849001869,
  "peak_tilt_rad": 0.6305496312957777,
  "peak_wheel_torque_nm": 6.137828826904297,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.59392381797079
}
```
