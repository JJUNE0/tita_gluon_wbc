# tita_flash_sac_193248_068255_model_60000_v02_s911_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 9b0d8897472dc567619d49df3e6df08813dcbb15b018f23ed58060e92e1b139b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_60000_v02_s911_300s",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_60000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 911,
    "estimator": "fk",
    "runtime": true,
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
  "checkpoint_sha256": "9b0d8897472dc567619d49df3e6df08813dcbb15b018f23ed58060e92e1b139b",
  "onnx_sha256": "bd80a0d28ffd69209d8e2ef2f6d867ca3f72a00abd0a3c8dbb0b6def13e19b7e",
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
  "initial_physics_sha256": "92ee2659ac20f3135e8a2ec13865cef4b86a3b1eebd246135b650acfbd5c4b02",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.003124569301248473,
  "max_drift_m": 0.0050821377509187495,
  "radial_IAE_m_s": 0.5754588696422539,
  "signed_longitudinal_delta_m": 0.0028153182990674707,
  "tail_speed_mean_m_s": 8.211706190687246e-06,
  "tail_speed_rms_m_s": 8.215741063940234e-06,
  "tail_sensor_speed_mean_m_s": 7.873616700877833e-06,
  "tail_fk_speed_mean_m_s": 9.963309938467916e-06,
  "peak_tilt_rad": 0.039298481993846,
  "peak_wheel_torque_nm": 0.1402466893196106,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.033901537400722735,
  "final_integral_m_s": 0.03388253726865156,
  "elapsed_wall_s": 89.72744441399118
}
```
