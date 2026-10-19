# tita_flash_sac_115632_883848_model_20000_kick-0.2_v03_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: c067f9f1969ee73b6c4bffcaac2a22db6c94c15ed22bacc3ce5bbde40776fe1b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_20000_kick-0.2_v03_s917",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_20000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 917,
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
      "slew": 2.0,
      "seed_gain": 3.0
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
  "initial_physics_sha256": "08168cb2cbebf78f9eb6b4cd3fe9dad7c96034064be71c27dc05bec14556a399",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.03242546816113202,
  "max_drift_m": 0.05865186484320827,
  "radial_IAE_m_s": 1.979920213335408,
  "signed_longitudinal_delta_m": -0.032418455500717445,
  "tail_speed_mean_m_s": 3.1084118822237898e-06,
  "tail_speed_rms_m_s": 0.00024286667263366226,
  "tail_sensor_speed_mean_m_s": 9.232540139638155e-06,
  "tail_fk_speed_mean_m_s": 1.8716831363585438e-05,
  "peak_tilt_rad": 0.14624264817138632,
  "peak_wheel_torque_nm": 1.19843590259552,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.26902372492963844,
  "final_integral_m_s": 0.26902372492963844,
  "elapsed_wall_s": 10.489309273019899
}
```
