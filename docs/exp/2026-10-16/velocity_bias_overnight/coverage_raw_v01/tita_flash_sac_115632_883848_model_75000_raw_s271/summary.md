# tita_flash_sac_115632_883848_model_75000_raw_s271

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 381e846e3ffb1d5a9ed629c02b55c9740ec3c5b089ca443f38b3d73b6abbd730

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_75000_raw_s271",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_75000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 271,
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.05,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
    },
    "estimator": "raw"
  },
  "checkpoint_sha256": "381e846e3ffb1d5a9ed629c02b55c9740ec3c5b089ca443f38b3d73b6abbd730",
  "onnx_sha256": "2bd3f78d10bc3b7cc4e50272d0289147f13b0a62ac6730048ba653ae53f35114",
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
  "initial_physics_sha256": "94f015b9d470467374b6eab3b3342ccb8c9780d87777117294b2fb185217d7eb",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.0005690636658541691,
  "max_drift_m": 0.0017654488789949846,
  "radial_IAE_m_s": 0.03821420105170437,
  "signed_longitudinal_delta_m": 0.0002528890069126734,
  "tail_speed_mean_m_s": 4.133980140087254e-05,
  "tail_speed_rms_m_s": 0.0019557166307156847,
  "tail_sensor_speed_mean_m_s": 0.00041196601717192674,
  "tail_fk_speed_mean_m_s": 3.041746749720805e-05,
  "peak_tilt_rad": 0.05547716015599491,
  "peak_wheel_torque_nm": 0.7788196802139282,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.13701998263546292,
  "final_integral_m_s": 0.016049648602057466,
  "elapsed_wall_s": 4.393702509987634
}
```
