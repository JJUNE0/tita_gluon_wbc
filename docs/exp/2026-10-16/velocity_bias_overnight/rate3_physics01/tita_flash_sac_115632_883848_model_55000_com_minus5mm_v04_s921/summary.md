# tita_flash_sac_115632_883848_model_55000_com_minus5mm_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: bb5591e26f71829becb4dab5c4e2effcd37054b9722c650dbf0e2ba993329aa7

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_55000_com_minus5mm_v04_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_55000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "com": -0.005
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
  "initial_physics_sha256": "a413b3eec757dc2843d68e25093870e4e17f9b6b82419eecb830f0f75ce6fe84",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.004638931230834668,
  "max_drift_m": 0.037026220313482336,
  "radial_IAE_m_s": 0.25398868852584333,
  "signed_longitudinal_delta_m": -0.004601122417818642,
  "tail_speed_mean_m_s": -4.0894846844900924e-05,
  "tail_speed_rms_m_s": 4.094553129733883e-05,
  "tail_sensor_speed_mean_m_s": -3.8543978513708754e-05,
  "tail_fk_speed_mean_m_s": -3.4807321235730786e-05,
  "peak_tilt_rad": 0.08623096017187937,
  "peak_wheel_torque_nm": 0.7641527056694031,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.195983612606345,
  "final_integral_m_s": 0.195983612606345,
  "elapsed_wall_s": 7.532555905985646
}
```
