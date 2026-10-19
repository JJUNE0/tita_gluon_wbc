# tita_flash_sac_115632_883848_model_20000_mass115_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: c067f9f1969ee73b6c4bffcaac2a22db6c94c15ed22bacc3ce5bbde40776fe1b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_20000_mass115_baseline_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_20000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "mass": 1.15
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
  "initial_physics_sha256": "af3ebece43c877657158a470a47804925ea216270fb60e992c1e9e6f16120c3e",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 9.65849924552356,
  "max_drift_m": 9.65849924552356,
  "radial_IAE_m_s": 288.71473157076974,
  "signed_longitudinal_delta_m": 9.565825403864721,
  "tail_speed_mean_m_s": 0.16293699097628614,
  "tail_speed_rms_m_s": 0.16293753255757604,
  "tail_sensor_speed_mean_m_s": 0.1624941786476837,
  "tail_fk_speed_mean_m_s": 0.16257906925401835,
  "peak_tilt_rad": 0.192632514361484,
  "peak_wheel_torque_nm": 0.6447126865386963,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 10.431527421984356
}
```
