# tita_flash_sac_115632_883848_model_45000_tau0.1_entry12

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 43062a7c7858bfeb0cce0542eb1f4a18dfcde51a093f58d89c7806ec35643067

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_45000_tau0.1_entry12",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_45000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 271,
    "estimator": "fk",
    "runtime": true,
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
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
  "initial_physics_sha256": "42e8e55199931e26f574a4498ced00a724bc36c4b3e9a1ea1a0a7a30ad251ac6",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.004653514827820681,
  "max_drift_m": 0.014237560495800617,
  "radial_IAE_m_s": 0.5030529293693407,
  "signed_longitudinal_delta_m": 0.0037580447645268224,
  "tail_speed_mean_m_s": -0.00021852908089399923,
  "tail_speed_rms_m_s": 0.008996346303079009,
  "tail_sensor_speed_mean_m_s": -0.0019284470304263925,
  "tail_fk_speed_mean_m_s": 5.2612428855065484e-05,
  "peak_tilt_rad": 0.04345773232277761,
  "peak_wheel_torque_nm": 3.408165693283081,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.16656666484228613,
  "final_integral_m_s": 0.14659920016653072,
  "elapsed_wall_s": 5.953298042004462
}
```
