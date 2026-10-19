# tita_flash_sac_115632_883848_model_90000_com_plus5mm_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 4930085834f72c133d65563169762514342959361a6d71630216f5f608b0531f

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_90000_com_plus5mm_v02_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_90000",
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
  "checkpoint_sha256": "4930085834f72c133d65563169762514342959361a6d71630216f5f608b0531f",
  "onnx_sha256": "1d6ffa5d91a15cf74e2abf755c367c1fb151f6e3c740618a6e1fb2fbf28f9379",
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
  "initial_physics_sha256": "791cdca2d85a59d5de1d410feb895df4126667f3caf2ac666f1c53cf7cc75db3",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.041636034946495856,
  "max_drift_m": 0.055602115133672136,
  "radial_IAE_m_s": 2.4704076121437755,
  "signed_longitudinal_delta_m": 0.04163595241168316,
  "tail_speed_mean_m_s": 1.3260550177435482e-05,
  "tail_speed_rms_m_s": 1.4028816365557323e-05,
  "tail_sensor_speed_mean_m_s": 1.3065839390557698e-05,
  "tail_fk_speed_mean_m_s": 1.4048729855128105e-05,
  "peak_tilt_rad": 0.07107653240247669,
  "peak_wheel_torque_nm": 0.6199653744697571,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.4268629464664151,
  "final_integral_m_s": 0.42683021069286836,
  "elapsed_wall_s": 18.219923663011286
}
```
