# tita_flash_sac_115632_883848_model_10000_kick-0.2_v04_s922

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 48a0379d0b30385cff5ccfe473d0ee136f303e640a505719a82bad5a3e3178a5

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_10000_kick-0.2_v04_s922",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_10000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 922,
    "estimator": "fk",
    "guarded": true,
    "kick": -0.2,
    "law": {
      "kp": 0.0,
      "ki": 4.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 3.0,
      "seed_gain": 3.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
  },
  "checkpoint_sha256": "48a0379d0b30385cff5ccfe473d0ee136f303e640a505719a82bad5a3e3178a5",
  "onnx_sha256": "06e48800bb84c9f9275464d939d3614105bfbc1bbe6af1e92522c94faa5f1e15",
  "input_columns": [
    "velocity_bias_m_s",
    "filtered_velocity_m_s",
    "integral_m_s"
  ],
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
  "initial_physics_sha256": "01aaf0f24bf1b13a3418bc0ea09827d991e34267d2eea4e2e11cb079f2287a95",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.08084053224235027,
  "max_drift_m": 0.10520880715394297,
  "radial_IAE_m_s": 5.18493252981507,
  "signed_longitudinal_delta_m": 0.08082669668384455,
  "tail_speed_mean_m_s": -0.0008453860419914952,
  "tail_speed_rms_m_s": 0.017519135863582832,
  "tail_sensor_speed_mean_m_s": -0.0009379635518237565,
  "tail_fk_speed_mean_m_s": -0.0009415494916573087,
  "peak_tilt_rad": 0.1189700539323173,
  "peak_wheel_torque_nm": 3.221964120864868,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.3445417456037336,
  "final_integral_m_s": 0.3445417456037336,
  "elapsed_wall_s": 9.098937756964006
}
```
