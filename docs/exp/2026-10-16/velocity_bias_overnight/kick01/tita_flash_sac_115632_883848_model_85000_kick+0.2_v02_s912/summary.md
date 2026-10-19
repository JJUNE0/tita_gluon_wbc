# tita_flash_sac_115632_883848_model_85000_kick+0.2_v02_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d1530cc4acd3186dfa88b59087ef850fd51f024ba7eba3252bc14a6549cc77d7

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_85000_kick+0.2_v02_s912",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_85000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 912,
    "estimator": "fk",
    "runtime": true,
    "kick": 0.2,
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
  "checkpoint_sha256": "d1530cc4acd3186dfa88b59087ef850fd51f024ba7eba3252bc14a6549cc77d7",
  "onnx_sha256": "1ed320e4785fe0edd047b9aa7e4185e975602f208fcf3deca0a9aa486c76114c",
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
  "initial_physics_sha256": "3146ae41a897386d9315f3b0cc8706649c01b9109aa733713d29a8cf8794c4f6",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.05876031425827006,
  "max_drift_m": 0.13339738161775097,
  "radial_IAE_m_s": 3.5974513670347408,
  "signed_longitudinal_delta_m": 0.058753009938409914,
  "tail_speed_mean_m_s": -7.485396606327503e-07,
  "tail_speed_rms_m_s": 3.925557854697368e-06,
  "tail_sensor_speed_mean_m_s": -7.079080904711222e-07,
  "tail_fk_speed_mean_m_s": -3.9249443629873787e-07,
  "peak_tilt_rad": 0.09137575508841622,
  "peak_wheel_torque_nm": 2.151268482208252,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.5848050730690476,
  "final_integral_m_s": 0.5847961519225905,
  "elapsed_wall_s": 20.642961748002563
}
```
