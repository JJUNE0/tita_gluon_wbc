# tita_flash_sac_115632_883848_model_10000_baseline_s911_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 48a0379d0b30385cff5ccfe473d0ee136f303e640a505719a82bad5a3e3178a5

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_10000_baseline_s911_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_10000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 911,
    "estimator": "fk",
    "runtime": false,
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
  "initial_physics_sha256": "ac71e583e26fbf2da3ad7475ed10fa6bf6cf734383d330cb67b04a6a11c39af3",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 6.245033081989057,
  "max_drift_m": 6.245033081989057,
  "radial_IAE_m_s": 968.632509591707,
  "signed_longitudinal_delta_m": 6.2207192746825495,
  "tail_speed_mean_m_s": 0.019814271651254312,
  "tail_speed_rms_m_s": 0.022208988784353432,
  "tail_sensor_speed_mean_m_s": 0.018885848733242224,
  "tail_fk_speed_mean_m_s": 0.019726862533669048,
  "peak_tilt_rad": 0.1150628924903796,
  "peak_wheel_torque_nm": 2.842381477355957,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 58.718966286978684
}
```
