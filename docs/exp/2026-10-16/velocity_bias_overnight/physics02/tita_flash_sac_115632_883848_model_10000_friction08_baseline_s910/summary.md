# tita_flash_sac_115632_883848_model_10000_friction08_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 48a0379d0b30385cff5ccfe473d0ee136f303e640a505719a82bad5a3e3178a5

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_10000_friction08_baseline_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_10000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "friction": 0.8
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
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
  "initial_physics_sha256": "b1c4dd6311fd921cce42a39eec7947078c8035e531e7cdca19ca703a78d89ce0",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 1.4489561376118056,
  "max_drift_m": 1.4489561376118056,
  "radial_IAE_m_s": 45.287108734687806,
  "signed_longitudinal_delta_m": 1.4479428012534483,
  "tail_speed_mean_m_s": 0.022252200557366614,
  "tail_speed_rms_m_s": 0.024563221754623363,
  "tail_sensor_speed_mean_m_s": 0.02090030652232038,
  "tail_fk_speed_mean_m_s": 0.022220371617362178,
  "peak_tilt_rad": 0.11507330025582352,
  "peak_wheel_torque_nm": 2.8356435298919678,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 16.021331255033147
}
```
