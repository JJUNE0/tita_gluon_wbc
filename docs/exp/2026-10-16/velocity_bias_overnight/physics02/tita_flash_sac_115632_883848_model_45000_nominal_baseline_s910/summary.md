# tita_flash_sac_115632_883848_model_45000_nominal_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 43062a7c7858bfeb0cce0542eb1f4a18dfcde51a093f58d89c7806ec35643067

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_45000_nominal_baseline_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_45000",
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
  "checkpoint_sha256": "43062a7c7858bfeb0cce0542eb1f4a18dfcde51a093f58d89c7806ec35643067",
  "onnx_sha256": "7b25c8c9afe56cdbfe483aa15167008f11b20e96722bf811b19fa3d80bf0e8e5",
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
  "initial_physics_sha256": "dc6f3627330a3ae8592862b8dfc9abe5e0cb72b8b6c12ce0c40ada007c681c17",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 2.4743033818718123,
  "max_drift_m": 2.4743033818718123,
  "radial_IAE_m_s": 73.1709839765669,
  "signed_longitudinal_delta_m": 2.4128277891031957,
  "tail_speed_mean_m_s": 0.042335629136978546,
  "tail_speed_rms_m_s": 0.042945883058012814,
  "tail_sensor_speed_mean_m_s": 0.041612278572706614,
  "tail_fk_speed_mean_m_s": 0.042454569371876125,
  "peak_tilt_rad": 0.05210086724330809,
  "peak_wheel_torque_nm": 2.6974070072174072,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 8.326703422993887
}
```
