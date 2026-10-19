# tita_flash_sac_115632_883848_model_45000_v04_s918_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 43062a7c7858bfeb0cce0542eb1f4a18dfcde51a093f58d89c7806ec35643067

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_45000_v04_s918_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_45000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 918,
    "estimator": "fk",
    "runtime": true,
    "law": {
      "kp": 0.0,
      "ki": 4.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 3.0,
      "seed_gain": 3.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f",
    "controller_source_sha256": "4e549f65ed2d2f9b18e668a01f29676c85b4cabf11d295c503fd83ad71b2171f"
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
  "initial_physics_sha256": "6f721d9f26204e40c5eb90545361dc8d9d2be1251ed98d0817c17de83733e34a",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.01835408492375328,
  "max_drift_m": 0.03363111439107666,
  "radial_IAE_m_s": 3.509246276349164,
  "signed_longitudinal_delta_m": 0.006872787371397145,
  "tail_speed_mean_m_s": -0.00038620261810380575,
  "tail_speed_rms_m_s": 0.01132435051778972,
  "tail_sensor_speed_mean_m_s": -0.0024443201203654236,
  "tail_fk_speed_mean_m_s": 3.660179249429621e-05,
  "peak_tilt_rad": 0.04862097759266337,
  "peak_wheel_torque_nm": 4.630008697509766,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.03591619256555427,
  "final_integral_m_s": -0.03591619256555427,
  "elapsed_wall_s": 54.07936157495715
}
```
