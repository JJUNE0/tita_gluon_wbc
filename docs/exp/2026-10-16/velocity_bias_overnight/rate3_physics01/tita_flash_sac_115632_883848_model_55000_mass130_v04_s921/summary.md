# tita_flash_sac_115632_883848_model_55000_mass130_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: bb5591e26f71829becb4dab5c4e2effcd37054b9722c650dbf0e2ba993329aa7

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_55000_mass130_v04_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_55000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "mass": 1.3
    },
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
  "initial_physics_sha256": "b60b60120d3b32abcd66b2e2f057fe060547ce44095d72c096c60bbf71fd902f",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.009268907788752202,
  "max_drift_m": 0.019942254895941113,
  "radial_IAE_m_s": 0.599613285078624,
  "signed_longitudinal_delta_m": 0.009268056583607546,
  "tail_speed_mean_m_s": -1.897806575661851e-05,
  "tail_speed_rms_m_s": 1.8995333836246814e-05,
  "tail_sensor_speed_mean_m_s": -1.850018995878038e-05,
  "tail_fk_speed_mean_m_s": -1.806160341387811e-05,
  "peak_tilt_rad": 0.15412756491567858,
  "peak_wheel_torque_nm": 0.7599875330924988,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.12767639913729678,
  "final_integral_m_s": -0.12767639913729678,
  "elapsed_wall_s": 6.721117092994973
}
```
