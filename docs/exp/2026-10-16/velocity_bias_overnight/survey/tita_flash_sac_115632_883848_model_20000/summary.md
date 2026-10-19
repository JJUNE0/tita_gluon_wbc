# tita_flash_sac_115632_883848_model_20000

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: c067f9f1969ee73b6c4bffcaac2a22db6c94c15ed22bacc3ce5bbde40776fe1b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_20000",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_20000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 270,
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
  "initial_physics_sha256": "9d5331b8e158be3376a7b05b7430acd282bda9e94b3e8a248010eb40593a7aca",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 14.434344983407879,
  "max_drift_m": 14.434344983407879,
  "radial_IAE_m_s": 437.759198366866,
  "signed_longitudinal_delta_m": 13.606541714930895,
  "tail_speed_mean_m_s": 0.2454359589453098,
  "tail_speed_rms_m_s": 0.2454359589705633,
  "tail_sensor_speed_mean_m_s": 0.24490647231956467,
  "tail_fk_speed_mean_m_s": 0.24487587146703155,
  "peak_tilt_rad": 0.17105430087759155,
  "peak_wheel_torque_nm": 0.15351414680480957,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 4.783483595005237
}
```
