# tita_flash_sac_115632_883848_model_20000_baseline_s911_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: c067f9f1969ee73b6c4bffcaac2a22db6c94c15ed22bacc3ce5bbde40776fe1b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_20000_baseline_s911_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_20000",
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
  "checkpoint_sha256": "c067f9f1969ee73b6c4bffcaac2a22db6c94c15ed22bacc3ce5bbde40776fe1b",
  "onnx_sha256": "3239fc95c745b5b2f5eed89d510784b637873c36570ad233e58125f30736faf4",
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
  "initial_physics_sha256": "48fc3376f70f5f4b9c64c8d97b468fcb7386c8555349e912eb02119b467307f6",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 41.152625719096136,
  "max_drift_m": 41.891676939346496,
  "radial_IAE_m_s": 8473.091322757402,
  "signed_longitudinal_delta_m": -4.586106061061098,
  "tail_speed_mean_m_s": 0.24543106559999742,
  "tail_speed_rms_m_s": 0.24543106560409159,
  "tail_sensor_speed_mean_m_s": 0.24490154346679455,
  "tail_fk_speed_mean_m_s": 0.24487098792235618,
  "peak_tilt_rad": 0.17105545141433054,
  "peak_wheel_torque_nm": 0.369464635848999,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 49.77970411395654
}
```
