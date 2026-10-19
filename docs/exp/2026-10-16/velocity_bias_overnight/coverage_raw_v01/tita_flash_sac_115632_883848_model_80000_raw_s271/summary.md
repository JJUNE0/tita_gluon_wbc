# tita_flash_sac_115632_883848_model_80000_raw_s271

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 80677a4fd403aad22ca310d644998b9b9a686da481d6d95eaf8cc02aa67afadc

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_80000_raw_s271",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_80000",
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
  "checkpoint_sha256": "80677a4fd403aad22ca310d644998b9b9a686da481d6d95eaf8cc02aa67afadc",
  "onnx_sha256": "c7a83d6c9814cc6aa8357e4b0215d65d880dd6b756de2de920967396e901c93b",
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
  "initial_physics_sha256": "7615c78b917077191c5976ee5ca765151e46a2561d3d77c8954c061526efe36d",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.08163323834761795,
  "max_drift_m": 0.108532916175553,
  "radial_IAE_m_s": 4.792534941922929,
  "signed_longitudinal_delta_m": 0.08160502213892336,
  "tail_speed_mean_m_s": 5.522048564529797e-05,
  "tail_speed_rms_m_s": 5.5264010375400156e-05,
  "tail_sensor_speed_mean_m_s": 5.4864773907618215e-05,
  "tail_fk_speed_mean_m_s": 5.51807165402373e-05,
  "peak_tilt_rad": 0.08579146193334819,
  "peak_wheel_torque_nm": 1.4335376024246216,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.8337161882507392,
  "final_integral_m_s": 0.8336040893810001,
  "elapsed_wall_s": 4.457477974006906
}
```
