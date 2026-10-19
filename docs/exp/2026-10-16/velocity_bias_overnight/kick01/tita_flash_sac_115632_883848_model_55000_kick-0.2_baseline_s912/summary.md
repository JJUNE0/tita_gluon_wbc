# tita_flash_sac_115632_883848_model_55000_kick-0.2_baseline_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: bb5591e26f71829becb4dab5c4e2effcd37054b9722c650dbf0e2ba993329aa7

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_55000_kick-0.2_baseline_s912",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_55000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 912,
    "estimator": "fk",
    "runtime": false,
    "kick": -0.2,
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "bb5591e26f71829becb4dab5c4e2effcd37054b9722c650dbf0e2ba993329aa7",
  "onnx_sha256": "8e2044f08b14f84be2b6152fb6085b58a0f6e377394a8fa0f7c69ebac1c08718",
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
  "initial_physics_sha256": "cda5e9551ff0d97bf1bad8beb0f481eb566802d90c0fbf35b2762bddc61612bd",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 6.567975013073415,
  "max_drift_m": 6.567975013073415,
  "radial_IAE_m_s": 191.6544513819856,
  "signed_longitudinal_delta_m": 6.469583680023663,
  "tail_speed_mean_m_s": 0.11306336269498402,
  "tail_speed_rms_m_s": 0.11306337627236776,
  "tail_sensor_speed_mean_m_s": 0.11281936360171604,
  "tail_fk_speed_mean_m_s": 0.11282087161105568,
  "peak_tilt_rad": 0.0908871034850467,
  "peak_wheel_torque_nm": 1.774326205253601,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 13.101307932054624
}
```
