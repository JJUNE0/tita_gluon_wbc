# tita_flash_sac_115632_883848_model_30000_com_plus5mm_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: ecff0682f7eaeee36f7e64c94170672ae7e912f30c8502429bab1e017f7ca17a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_30000_com_plus5mm_baseline_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_30000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "com": 0.005
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "ecff0682f7eaeee36f7e64c94170672ae7e912f30c8502429bab1e017f7ca17a",
  "onnx_sha256": "e68dce44a40c95e38733c80c73616e51e12114a29c11f53063c1d02eb989061e",
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
  "initial_physics_sha256": "37feae07bf0aa4da1ad5c104263d32b7a913db2905ede30b11240973b3fcab54",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 15.148328770716269,
  "max_drift_m": 15.148328770716269,
  "radial_IAE_m_s": 457.94745092504434,
  "signed_longitudinal_delta_m": 15.135454700031488,
  "tail_speed_mean_m_s": 0.2501893832047292,
  "tail_speed_rms_m_s": 0.2501894140027053,
  "tail_sensor_speed_mean_m_s": 0.24964749749422904,
  "tail_fk_speed_mean_m_s": 0.24964603726967569,
  "peak_tilt_rad": 0.12863097174390203,
  "peak_wheel_torque_nm": 0.15475642681121826,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 10.169814688968472
}
```
