# tita_flash_sac_193248_068255_model_55000_baseline_s911_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 02d44258f752e3d43bac0b8eba0ebb2b4c1d262d812cc040b22672a16cdb583c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_55000_baseline_s911_300s",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_55000",
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
  "checkpoint_sha256": "02d44258f752e3d43bac0b8eba0ebb2b4c1d262d812cc040b22672a16cdb583c",
  "onnx_sha256": "98bc9d9fb343d683cc0b87892391ac7fee7f391381ceff241490864772abca13",
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
  "initial_physics_sha256": "5ff582496223ab9b83920b453c08ae615f97604b688693de931ed7dbf1e3af8f",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 81.03518144305411,
  "max_drift_m": 81.03518144305411,
  "radial_IAE_m_s": 13177.648724750774,
  "signed_longitudinal_delta_m": 45.922725449203774,
  "tail_speed_mean_m_s": 0.3241111211977656,
  "tail_speed_rms_m_s": 0.3241111212012429,
  "tail_sensor_speed_mean_m_s": 0.32341028325782983,
  "tail_fk_speed_mean_m_s": 0.3234035964329439,
  "peak_tilt_rad": 0.1735490092991756,
  "peak_wheel_torque_nm": 0.2577481269836426,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 64.23418577300617
}
```
