# tita_flash_sac_115632_883848_model_45000_com_plus5mm_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 43062a7c7858bfeb0cce0542eb1f4a18dfcde51a093f58d89c7806ec35643067

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_45000_com_plus5mm_v02_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_45000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "com": 0.005
    },
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
  "initial_physics_sha256": "32fd4f89ddbf4dfc2ce3eb6650e73a0175be6673ab84f66b73642cb079f1a5ff",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.008523347525343242,
  "max_drift_m": 0.015978756180570645,
  "radial_IAE_m_s": 0.6365921813764993,
  "signed_longitudinal_delta_m": 0.007739126689754185,
  "tail_speed_mean_m_s": -0.0001437962044867507,
  "tail_speed_rms_m_s": 0.008991366017635357,
  "tail_sensor_speed_mean_m_s": 0.0013261077245072814,
  "tail_fk_speed_mean_m_s": 0.00015217189363176344,
  "peak_tilt_rad": 0.04155235094897436,
  "peak_wheel_torque_nm": 3.345609188079834,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.1874700805233058,
  "final_integral_m_s": 0.17980935686365176,
  "elapsed_wall_s": 12.441086206003092
}
```
