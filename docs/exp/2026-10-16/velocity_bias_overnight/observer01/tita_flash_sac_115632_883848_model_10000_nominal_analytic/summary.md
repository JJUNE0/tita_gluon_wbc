# tita_flash_sac_115632_883848_model_10000_nominal_analytic

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 48a0379d0b30385cff5ccfe473d0ee136f303e640a505719a82bad5a3e3178a5

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_10000_nominal_analytic",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_10000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 272,
    "estimator": "analytic",
    "physics": {},
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
  "initial_physics_sha256": "5523d2aec6fb2dc4e6586f5b2a6cdbe778ee02fc09a3e317ea9893687d563626",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.04232510330646699,
  "max_drift_m": 0.04344055098396069,
  "radial_IAE_m_s": 2.132260355068933,
  "signed_longitudinal_delta_m": 0.042324084063199305,
  "tail_speed_mean_m_s": 0.00025364191212497297,
  "tail_speed_rms_m_s": 0.01739397796393308,
  "tail_sensor_speed_mean_m_s": 0.0008957567005996586,
  "tail_fk_speed_mean_m_s": 4.19990606284632e-05,
  "peak_tilt_rad": 0.11299689354990083,
  "peak_wheel_torque_nm": 2.917219400405884,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.3018656493036284,
  "final_integral_m_s": 0.277167873034427,
  "elapsed_wall_s": 15.529780993994791
}
```
