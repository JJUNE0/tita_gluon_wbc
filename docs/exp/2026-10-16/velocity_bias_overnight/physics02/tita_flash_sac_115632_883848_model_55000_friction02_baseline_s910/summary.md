# tita_flash_sac_115632_883848_model_55000_friction02_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: bb5591e26f71829becb4dab5c4e2effcd37054b9722c650dbf0e2ba993329aa7

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_55000_friction02_baseline_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_55000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "friction": 0.2
    },
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
  "initial_physics_sha256": "b529b928de2d71af02109c000e95c58120dcffe89c0f5b5ad3f679ffc5c0b056",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.8922260697380313,
  "max_drift_m": 2.2722861338461513,
  "radial_IAE_m_s": 94.17819369034939,
  "signed_longitudinal_delta_m": -0.43956978694094867,
  "tail_speed_mean_m_s": 0.09103615416802721,
  "tail_speed_rms_m_s": 0.09103835742073074,
  "tail_sensor_speed_mean_m_s": 0.090884410878446,
  "tail_fk_speed_mean_m_s": 0.0909230936065422,
  "peak_tilt_rad": 0.0844771926872312,
  "peak_wheel_torque_nm": 0.16809391975402832,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 15.08620018500369
}
```
