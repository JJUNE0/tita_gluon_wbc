# tita_flash_sac_115632_883848_model_55000_nominal_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: bb5591e26f71829becb4dab5c4e2effcd37054b9722c650dbf0e2ba993329aa7

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_55000_nominal_v04_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_55000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": true,
    "physics": {},
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
  "checkpoint_sha256": "bb5591e26f71829becb4dab5c4e2effcd37054b9722c650dbf0e2ba993329aa7",
  "onnx_sha256": "8e2044f08b14f84be2b6152fb6085b58a0f6e377394a8fa0f7c69ebac1c08718",
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
  "initial_physics_sha256": "2f91a5052b2b26139fa507e553d311156e5bcfada6436263f49c374bff2ee93f",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.00846884064465342,
  "max_drift_m": 0.045712116883793126,
  "radial_IAE_m_s": 0.4899440706348854,
  "signed_longitudinal_delta_m": -0.008464389224591059,
  "tail_speed_mean_m_s": -4.087790956155424e-05,
  "tail_speed_rms_m_s": 4.107584188289355e-05,
  "tail_sensor_speed_mean_m_s": -3.997471983304671e-05,
  "tail_fk_speed_mean_m_s": -3.663915506318589e-05,
  "peak_tilt_rad": 0.08949491310578073,
  "peak_wheel_torque_nm": 0.9421278238296509,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.240901811895798,
  "final_integral_m_s": 0.240901811895798,
  "elapsed_wall_s": 6.015474830986932
}
```
