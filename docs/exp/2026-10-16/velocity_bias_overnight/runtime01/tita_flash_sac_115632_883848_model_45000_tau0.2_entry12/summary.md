# tita_flash_sac_115632_883848_model_45000_tau0.2_entry12

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 43062a7c7858bfeb0cce0542eb1f4a18dfcde51a093f58d89c7806ec35643067

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_45000_tau0.2_entry12",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_45000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 271,
    "estimator": "fk",
    "runtime": true,
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.2,
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
  "final_drift_m": 0.006772796264145004,
  "max_drift_m": 0.015478732399266368,
  "radial_IAE_m_s": 0.567906535228448,
  "signed_longitudinal_delta_m": 0.006451430906038819,
  "tail_speed_mean_m_s": -0.00013656430175812138,
  "tail_speed_rms_m_s": 0.008705000331766456,
  "tail_sensor_speed_mean_m_s": -0.0019027996938759874,
  "tail_fk_speed_mean_m_s": -0.00011017730060474796,
  "peak_tilt_rad": 0.041176025637180924,
  "peak_wheel_torque_nm": 3.08728289604187,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.14027005381574753,
  "final_integral_m_s": 0.15193878774024197,
  "elapsed_wall_s": 5.986597126990091
}
```
