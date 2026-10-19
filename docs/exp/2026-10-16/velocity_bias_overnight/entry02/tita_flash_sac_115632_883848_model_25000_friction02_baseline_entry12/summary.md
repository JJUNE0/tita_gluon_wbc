# tita_flash_sac_115632_883848_model_25000_friction02_baseline_entry12

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: fd99df31c9e160baa980cd421917f4536bfda16779ad79754dd3d4bf13c600b1

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_25000_friction02_baseline_entry12",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_25000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 272,
    "estimator": "fk",
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
  "initial_physics_sha256": "935833de9684b3951af9d10f1d663a6bd7a943221f6698776aa91bb0440f9c99",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.08780073336417676,
  "max_drift_m": 0.08796286827841737,
  "radial_IAE_m_s": 2.506473231887582,
  "signed_longitudinal_delta_m": -0.08771298043041553,
  "tail_speed_mean_m_s": -0.001506102138278907,
  "tail_speed_rms_m_s": 0.007948010400140237,
  "tail_sensor_speed_mean_m_s": 7.978407950216134,
  "tail_fk_speed_mean_m_s": 7.978361980707353,
  "peak_tilt_rad": 0.6305499703437909,
  "peak_wheel_torque_nm": 6.137836456298828,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 5.136713805026375
}
```
