# tita_flash_sac_115632_883848_model_20000_kick+0.2_baseline_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: c067f9f1969ee73b6c4bffcaac2a22db6c94c15ed22bacc3ce5bbde40776fe1b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_20000_kick+0.2_baseline_s912",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_20000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 912,
    "estimator": "fk",
    "runtime": false,
    "kick": 0.2,
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
  "initial_physics_sha256": "cbbf0f5450cc58411db483035017b7ff1836b26723ff26dc2ab70158cfa10f57",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 14.495483355327918,
  "max_drift_m": 14.495483355327918,
  "radial_IAE_m_s": 440.8044358603706,
  "signed_longitudinal_delta_m": 13.913953148323479,
  "tail_speed_mean_m_s": 0.24544175881916633,
  "tail_speed_rms_m_s": 0.24544175892893128,
  "tail_sensor_speed_mean_m_s": 0.2449122769836405,
  "tail_fk_speed_mean_m_s": 0.2448816586603076,
  "peak_tilt_rad": 0.1800651143909482,
  "peak_wheel_torque_nm": 2.21510648727417,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 10.680639034952037
}
```
