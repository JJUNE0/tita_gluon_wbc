# tita_flash_sac_115632_883848_model_20000_baseline_s918_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: c067f9f1969ee73b6c4bffcaac2a22db6c94c15ed22bacc3ce5bbde40776fe1b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_20000_baseline_s918_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_20000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 918,
    "estimator": "fk",
    "guarded": false,
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
  },
  "checkpoint_sha256": "c067f9f1969ee73b6c4bffcaac2a22db6c94c15ed22bacc3ce5bbde40776fe1b",
  "onnx_sha256": "3239fc95c745b5b2f5eed89d510784b637873c36570ad233e58125f30736faf4",
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
  "initial_physics_sha256": "76e3ee49bb2a73977ec541d378239579ec194398c4465b12e7f5b6e51b76770d",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 41.155730912016814,
  "max_drift_m": 41.894764021728946,
  "radial_IAE_m_s": 8473.651719176924,
  "signed_longitudinal_delta_m": -4.482200527866722,
  "tail_speed_mean_m_s": 0.2454310639056477,
  "tail_speed_rms_m_s": 0.2454310639099162,
  "tail_sensor_speed_mean_m_s": 0.24490154355819482,
  "tail_fk_speed_mean_m_s": 0.24487098664754903,
  "peak_tilt_rad": 0.1710555471841635,
  "peak_wheel_torque_nm": 0.36821115016937256,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 55.87293763901107
}
```
