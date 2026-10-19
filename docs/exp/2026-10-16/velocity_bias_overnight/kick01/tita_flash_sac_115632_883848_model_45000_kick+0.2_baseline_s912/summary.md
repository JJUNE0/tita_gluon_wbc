# tita_flash_sac_115632_883848_model_45000_kick+0.2_baseline_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 43062a7c7858bfeb0cce0542eb1f4a18dfcde51a093f58d89c7806ec35643067

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_45000_kick+0.2_baseline_s912",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_45000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 912,
    "estimator": "fk",
    "runtime": false,
    "kick": 0.2,
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
  "initial_physics_sha256": "17c59771012e5108ce0d4e74eb7eab3f19dbedc359879471bc841cabe01efa41",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 2.572504806732743,
  "max_drift_m": 2.572504806732743,
  "radial_IAE_m_s": 78.97658960677333,
  "signed_longitudinal_delta_m": 2.510889696545088,
  "tail_speed_mean_m_s": 0.04239505323778253,
  "tail_speed_rms_m_s": 0.04298599333447284,
  "tail_sensor_speed_mean_m_s": 0.04392825965827323,
  "tail_fk_speed_mean_m_s": 0.042394081728296,
  "peak_tilt_rad": 0.06305469422859433,
  "peak_wheel_torque_nm": 4.2606892585754395,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 8.610937041055877
}
```
