# tita_flash_sac_115632_883848_model_40000_v04_runtime_s920

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a4b5c15c3add7114e65d55cabbe505c0fffcd993df1b9162587e073cca97a891

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_40000_v04_runtime_s920",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_40000",
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
  "checkpoint_sha256": "a4b5c15c3add7114e65d55cabbe505c0fffcd993df1b9162587e073cca97a891",
  "onnx_sha256": "4722a7e5dc4a1d465689d98943ba5c9a40a7d45a99344f923f067d1cfa90fcb6",
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
  "initial_physics_sha256": "faa4505f30764f820dd607f938ca166dad33d2f215969b841503baf96330843c",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.004755080796352538,
  "max_drift_m": 0.03981511864500479,
  "radial_IAE_m_s": 0.4023587000885073,
  "signed_longitudinal_delta_m": -0.004751025701226748,
  "tail_speed_mean_m_s": 4.37296978133944e-05,
  "tail_speed_rms_m_s": 4.385226729964752e-05,
  "tail_sensor_speed_mean_m_s": 4.314339950741361e-05,
  "tail_fk_speed_mean_m_s": 4.55025213700224e-05,
  "peak_tilt_rad": 0.11348022927466328,
  "peak_wheel_torque_nm": 0.8961499333381653,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.23392113817189242,
  "final_integral_m_s": 0.23392113817189242,
  "elapsed_wall_s": 13.138701062009204
}
```
