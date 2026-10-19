# tita_flash_sac_115632_883848_model_10000_nominal_fk

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 48a0379d0b30385cff5ccfe473d0ee136f303e640a505719a82bad5a3e3178a5

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_10000_nominal_fk",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_10000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 272,
    "estimator": "fk",
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
  "final_drift_m": 0.03521940559994765,
  "max_drift_m": 0.03870240547129497,
  "radial_IAE_m_s": 2.0973704110596114,
  "signed_longitudinal_delta_m": 0.03513872640795894,
  "tail_speed_mean_m_s": 2.2787043600042973e-05,
  "tail_speed_rms_m_s": 0.016137025167929423,
  "tail_sensor_speed_mean_m_s": -0.0006195635919921695,
  "tail_fk_speed_mean_m_s": -0.00010073305047539718,
  "peak_tilt_rad": 0.11299712842783816,
  "peak_wheel_torque_nm": 2.942823648452759,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.27238896737396534,
  "final_integral_m_s": 0.2838492119465067,
  "elapsed_wall_s": 14.192569668986835
}
```
