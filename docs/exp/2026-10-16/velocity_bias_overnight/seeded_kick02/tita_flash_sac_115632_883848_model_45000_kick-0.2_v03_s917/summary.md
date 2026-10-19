# tita_flash_sac_115632_883848_model_45000_kick-0.2_v03_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 43062a7c7858bfeb0cce0542eb1f4a18dfcde51a093f58d89c7806ec35643067

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_45000_kick-0.2_v03_s917",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_45000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 917,
    "estimator": "fk",
    "guarded": true,
    "kick": -0.2,
    "law": {
      "kp": 0.0,
      "ki": 4.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0,
      "seed_gain": 3.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
  },
  "checkpoint_sha256": "43062a7c7858bfeb0cce0542eb1f4a18dfcde51a093f58d89c7806ec35643067",
  "onnx_sha256": "7b25c8c9afe56cdbfe483aa15167008f11b20e96722bf811b19fa3d80bf0e8e5",
  "input_columns": [
    "velocity_bias_m_s",
    "filtered_velocity_m_s",
    "integral_m_s"
  ],
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
  "initial_physics_sha256": "6ff96664336f59668c00b70abad85e3fbb9dd5e7f4e96d753c8af88984596612",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.0006146899567753433,
  "max_drift_m": 0.04828295733994629,
  "radial_IAE_m_s": 0.22798583802783837,
  "signed_longitudinal_delta_m": 0.0004482285502382522,
  "tail_speed_mean_m_s": -6.385011587229194e-05,
  "tail_speed_rms_m_s": 0.007465665033384268,
  "tail_sensor_speed_mean_m_s": 0.0012765293563863332,
  "tail_fk_speed_mean_m_s": 0.0001138000610823218,
  "peak_tilt_rad": 0.05724945453776886,
  "peak_wheel_torque_nm": 2.599616050720215,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.1527948698114911,
  "final_integral_m_s": 0.1527948698114911,
  "elapsed_wall_s": 10.615485676040407
}
```
