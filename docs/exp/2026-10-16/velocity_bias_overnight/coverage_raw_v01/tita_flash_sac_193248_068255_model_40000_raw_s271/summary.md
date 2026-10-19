# tita_flash_sac_193248_068255_model_40000_raw_s271

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 391b8791d73b9fecdb5fae3be4e3efe31b71440d770ca559d9a5a526ad37efb4

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_40000_raw_s271",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_40000",
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
  "checkpoint_sha256": "391b8791d73b9fecdb5fae3be4e3efe31b71440d770ca559d9a5a526ad37efb4",
  "onnx_sha256": "fb82f05252341f0576dd6277b7c6e5d77e7daea4d9d3f180fe72795b3f56c966",
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
  "initial_physics_sha256": "15c0feba8222f51867e02f95fda61b0fa089c77ffdd99e5ffb5b64e37e335e5d",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.022132987581883562,
  "max_drift_m": 0.061257735643490664,
  "radial_IAE_m_s": 1.2330532149265407,
  "signed_longitudinal_delta_m": 0.022052067500939347,
  "tail_speed_mean_m_s": -4.0637481187860164e-05,
  "tail_speed_rms_m_s": 0.024405057805568186,
  "tail_sensor_speed_mean_m_s": 4.935700314340635e-05,
  "tail_fk_speed_mean_m_s": 3.555318528849586e-05,
  "peak_tilt_rad": 0.11568766869641656,
  "peak_wheel_torque_nm": 1.5641957521438599,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.4686570304249676,
  "final_integral_m_s": 0.42637980742898546,
  "elapsed_wall_s": 4.382787927985191
}
```
