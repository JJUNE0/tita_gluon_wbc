# tita_flash_sac_115632_883848_model_45000

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 43062a7c7858bfeb0cce0542eb1f4a18dfcde51a093f58d89c7806ec35643067

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_45000",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_45000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 270,
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
  "initial_physics_sha256": "b991a318c6fe0b2bd656ca689c0e6229dc3d7c0169288218313af8cfa713d52d",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 2.5016163141388015,
  "max_drift_m": 2.5016163141388015,
  "radial_IAE_m_s": 74.54051833499292,
  "signed_longitudinal_delta_m": 2.459798604752413,
  "tail_speed_mean_m_s": 0.04225188292396288,
  "tail_speed_rms_m_s": 0.04282063358180346,
  "tail_sensor_speed_mean_m_s": 0.04274718961056699,
  "tail_fk_speed_mean_m_s": 0.04236886718025711,
  "peak_tilt_rad": 0.052067043058361184,
  "peak_wheel_torque_nm": 2.698324680328369,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 4.524434985010885
}
```
