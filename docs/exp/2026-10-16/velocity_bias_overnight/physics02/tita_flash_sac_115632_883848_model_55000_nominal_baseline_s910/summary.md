# tita_flash_sac_115632_883848_model_55000_nominal_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: bb5591e26f71829becb4dab5c4e2effcd37054b9722c650dbf0e2ba993329aa7

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_55000_nominal_baseline_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_55000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {},
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
  "initial_physics_sha256": "83a7d6ebf8520f7b71c929b1dbb222a95f62ca522182cc793cb0277088f788c1",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 6.714193557106239,
  "max_drift_m": 6.714193557106239,
  "radial_IAE_m_s": 200.25632751853016,
  "signed_longitudinal_delta_m": 6.635068315013096,
  "tail_speed_mean_m_s": 0.11305537429763741,
  "tail_speed_rms_m_s": 0.11305538986015536,
  "tail_sensor_speed_mean_m_s": 0.11281140056780904,
  "tail_fk_speed_mean_m_s": 0.11281289034025187,
  "peak_tilt_rad": 0.09090568867129378,
  "peak_wheel_torque_nm": 0.36017298698425293,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 8.02837322501
}
```
