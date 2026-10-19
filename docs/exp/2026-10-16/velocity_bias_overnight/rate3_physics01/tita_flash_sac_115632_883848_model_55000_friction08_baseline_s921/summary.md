# tita_flash_sac_115632_883848_model_55000_friction08_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: bb5591e26f71829becb4dab5c4e2effcd37054b9722c650dbf0e2ba993329aa7

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_55000_friction08_baseline_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_55000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "friction": 0.8
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
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
  "initial_physics_sha256": "b334fc3361da69b275cb1ec9deb29e3cefb52062345ceaee5f0650f62d36f3b2",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 6.64020769971215,
  "max_drift_m": 6.64020769971215,
  "radial_IAE_m_s": 196.8282387357637,
  "signed_longitudinal_delta_m": 6.178110610432003,
  "tail_speed_mean_m_s": 0.11301863453239114,
  "tail_speed_rms_m_s": 0.11301864507761532,
  "tail_sensor_speed_mean_m_s": 0.11277666064180443,
  "tail_fk_speed_mean_m_s": 0.11277807900483908,
  "peak_tilt_rad": 0.09068523482816948,
  "peak_wheel_torque_nm": 0.306962788105011,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 8.342579452029895
}
```
