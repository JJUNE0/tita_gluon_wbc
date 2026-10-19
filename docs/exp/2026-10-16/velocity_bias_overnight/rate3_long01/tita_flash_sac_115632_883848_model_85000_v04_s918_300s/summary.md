# tita_flash_sac_115632_883848_model_85000_v04_s918_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d1530cc4acd3186dfa88b59087ef850fd51f024ba7eba3252bc14a6549cc77d7

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_85000_v04_s918_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_85000",
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
  "checkpoint_sha256": "d1530cc4acd3186dfa88b59087ef850fd51f024ba7eba3252bc14a6549cc77d7",
  "onnx_sha256": "1ed320e4785fe0edd047b9aa7e4185e975602f208fcf3deca0a9aa486c76114c",
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
  "initial_physics_sha256": "e2ae3416dc46d5de0e2ba3bbc52d43fc2f9036bcf7591f0263ad014023bff704",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.10978780628017132,
  "max_drift_m": 0.10978780628017132,
  "radial_IAE_m_s": 29.807212734718316,
  "signed_longitudinal_delta_m": 0.10978081884512662,
  "tail_speed_mean_m_s": 7.929389177243259e-05,
  "tail_speed_rms_m_s": 7.929402275872325e-05,
  "tail_sensor_speed_mean_m_s": 7.854769103617363e-05,
  "tail_fk_speed_mean_m_s": 7.972892821365146e-05,
  "peak_tilt_rad": 0.06529365526101238,
  "peak_wheel_torque_nm": 0.4435664415359497,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.6444922148465925,
  "final_integral_m_s": 0.6444922148465925,
  "elapsed_wall_s": 51.28502438502619
}
```
