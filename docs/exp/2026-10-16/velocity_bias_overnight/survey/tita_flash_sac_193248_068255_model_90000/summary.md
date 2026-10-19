# tita_flash_sac_193248_068255_model_90000

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d94ec425dcab69bfb8001711468b6ca37297f4e1aec2e9b20535fd106ee98769

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_90000",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_90000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 270,
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "d94ec425dcab69bfb8001711468b6ca37297f4e1aec2e9b20535fd106ee98769",
  "onnx_sha256": "aff309a07b913000eb7916a9b3867232296f7834f48d5391c16e7ec4e09b84d2",
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
  "initial_physics_sha256": "c09c11ab3ebf4c552e2bc2d345652e86a06ef9d1630aa3d5fa63ce2089dcc322",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 13.283741902958369,
  "max_drift_m": 13.283741902958369,
  "radial_IAE_m_s": 396.45421728108965,
  "signed_longitudinal_delta_m": 13.245248284151183,
  "tail_speed_mean_m_s": 0.22374907524872042,
  "tail_speed_rms_m_s": 0.2237491135124216,
  "tail_sensor_speed_mean_m_s": 0.2232650200133419,
  "tail_fk_speed_mean_m_s": 0.22326273183516873,
  "peak_tilt_rad": 0.11201321500081218,
  "peak_wheel_torque_nm": 0.2355440855026245,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 5.142210663005244
}
```
