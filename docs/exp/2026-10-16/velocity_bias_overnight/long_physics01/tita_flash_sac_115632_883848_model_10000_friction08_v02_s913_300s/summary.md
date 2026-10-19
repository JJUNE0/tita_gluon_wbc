# tita_flash_sac_115632_883848_model_10000_friction08_v02_s913_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 48a0379d0b30385cff5ccfe473d0ee136f303e640a505719a82bad5a3e3178a5

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_10000_friction08_v02_s913_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_10000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 913,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "friction": 0.8
    },
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
    }
  },
  "checkpoint_sha256": "48a0379d0b30385cff5ccfe473d0ee136f303e640a505719a82bad5a3e3178a5",
  "onnx_sha256": "06e48800bb84c9f9275464d939d3614105bfbc1bbe6af1e92522c94faa5f1e15",
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
  "initial_physics_sha256": "f161ff51b00b3adbc063135bb61b363f579c6fc84619ebbd5fe2ca62c4ca1f34",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.06086862561569267,
  "max_drift_m": 0.06092656335536397,
  "radial_IAE_m_s": 13.324084243437,
  "signed_longitudinal_delta_m": 0.06074485506630308,
  "tail_speed_mean_m_s": 0.00015372885437400416,
  "tail_speed_rms_m_s": 0.014219811996423425,
  "tail_sensor_speed_mean_m_s": 0.000964786007547618,
  "tail_fk_speed_mean_m_s": 3.874924276361218e-05,
  "peak_tilt_rad": 0.11337900270240331,
  "peak_wheel_torque_nm": 2.941329002380371,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.27695206941331896,
  "final_integral_m_s": 0.2948009353160568,
  "elapsed_wall_s": 59.850415169028565
}
```
