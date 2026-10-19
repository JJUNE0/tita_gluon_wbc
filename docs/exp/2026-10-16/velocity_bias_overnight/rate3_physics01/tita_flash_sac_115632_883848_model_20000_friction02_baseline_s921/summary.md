# tita_flash_sac_115632_883848_model_20000_friction02_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: c067f9f1969ee73b6c4bffcaac2a22db6c94c15ed22bacc3ce5bbde40776fe1b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_20000_friction02_baseline_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_20000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "friction": 0.2
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
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
  "initial_physics_sha256": "a8cd85162e23328fc0277edc7ba2b89ec9dac7fc6717b99825ae4deb3b1d955b",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 14.124222711453687,
  "max_drift_m": 14.124222711453687,
  "radial_IAE_m_s": 435.4044503387454,
  "signed_longitudinal_delta_m": 11.313490247457572,
  "tail_speed_mean_m_s": 0.25092908192987456,
  "tail_speed_rms_m_s": 0.25092908193642305,
  "tail_sensor_speed_mean_m_s": 0.25072366522147876,
  "tail_fk_speed_mean_m_s": 0.2507753607005217,
  "peak_tilt_rad": 0.17741235431817293,
  "peak_wheel_torque_nm": 0.23092985153198242,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 10.858381735975854
}
```
