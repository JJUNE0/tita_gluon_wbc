# tita_flash_sac_115632_883848_model_65000_v04_runtime_s920

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a28e8551929d9a4412f571a2e91577da75879477c15d61f0774ab6f05354dff3

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_65000_v04_runtime_s920",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_65000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 920,
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
  "checkpoint_sha256": "a28e8551929d9a4412f571a2e91577da75879477c15d61f0774ab6f05354dff3",
  "onnx_sha256": "7cc289e8aee44513f1e29487c7522e96c762174e2444aedaa7aea78b3a66a3ec",
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
  "initial_physics_sha256": "5eee42b224f39ff1c89d01bc79eae531a3cfad43e6e5a9cc93734b8fd1b6a79a",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.00125785795969908,
  "max_drift_m": 0.0111395909259852,
  "radial_IAE_m_s": 0.05322377713840689,
  "signed_longitudinal_delta_m": -0.0012401147325944097,
  "tail_speed_mean_m_s": -2.470293584437461e-05,
  "tail_speed_rms_m_s": 2.4729879452091934e-05,
  "tail_sensor_speed_mean_m_s": -2.443306117977818e-05,
  "tail_fk_speed_mean_m_s": -2.5617287197005868e-05,
  "peak_tilt_rad": 0.05682540218071597,
  "peak_wheel_torque_nm": 0.3475643992424011,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.04969347646239652,
  "final_integral_m_s": 0.04969347646239652,
  "elapsed_wall_s": 12.120647025993094
}
```
