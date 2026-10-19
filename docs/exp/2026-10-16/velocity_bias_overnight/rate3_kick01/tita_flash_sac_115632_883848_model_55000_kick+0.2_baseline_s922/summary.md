# tita_flash_sac_115632_883848_model_55000_kick+0.2_baseline_s922

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: bb5591e26f71829becb4dab5c4e2effcd37054b9722c650dbf0e2ba993329aa7

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_55000_kick+0.2_baseline_s922",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_55000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 922,
    "estimator": "fk",
    "guarded": false,
    "kick": 0.2,
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
  "initial_physics_sha256": "a8e285b1757f53011999d4b4c4e1ebf7e3ff59daa444781ec4e81dc4b372432a",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 6.847867008028894,
  "max_drift_m": 6.847867008028894,
  "radial_IAE_m_s": 208.18960769122637,
  "signed_longitudinal_delta_m": 6.774940173629618,
  "tail_speed_mean_m_s": 0.11305004518313745,
  "tail_speed_rms_m_s": 0.11305006194554103,
  "tail_sensor_speed_mean_m_s": 0.11280608268100634,
  "tail_fk_speed_mean_m_s": 0.11280756676376691,
  "peak_tilt_rad": 0.11500488653273222,
  "peak_wheel_torque_nm": 1.8283149003982544,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 8.80865358299343
}
```
