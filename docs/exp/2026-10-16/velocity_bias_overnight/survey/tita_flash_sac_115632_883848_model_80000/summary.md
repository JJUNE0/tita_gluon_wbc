# tita_flash_sac_115632_883848_model_80000

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 80677a4fd403aad22ca310d644998b9b9a686da481d6d95eaf8cc02aa67afadc

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_80000",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_80000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 270,
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
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
  "initial_physics_sha256": "81e04513edf1410cdb1b26e7745713910e41dd2acb40931eb776c481ba016a03",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 11.840425567916775,
  "max_drift_m": 11.840425567916775,
  "radial_IAE_m_s": 352.38034543495905,
  "signed_longitudinal_delta_m": 11.835337559374596,
  "tail_speed_mean_m_s": 0.19987654670558083,
  "tail_speed_rms_m_s": 0.19987666620939826,
  "tail_sensor_speed_mean_m_s": 0.19944477362864874,
  "tail_fk_speed_mean_m_s": 0.19944383795793086,
  "peak_tilt_rad": 0.08594875477979591,
  "peak_wheel_torque_nm": 0.2691711187362671,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 4.517051322036423
}
```
