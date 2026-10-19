# tita_flash_sac_115632_883848_model_35000_friction02_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 04d8993b85810ece43a5d202a8a86b46097dcc9e30ce2c7825e73f538f9beab6

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_35000_friction02_v04_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_35000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "friction": 0.2
    },
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
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
  },
  "checkpoint_sha256": "04d8993b85810ece43a5d202a8a86b46097dcc9e30ce2c7825e73f538f9beab6",
  "onnx_sha256": "3ce2f1cc7a17e8f712ba06efe9dc56bd55d6b0090b07942bae3238a59fef56e0",
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
  "initial_physics_sha256": "8532673b10974d7c4063a49bfdabb3dddb7cb60aa128d8975c6cdfb6fc94aa6a",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.009015173888346507,
  "max_drift_m": 0.07685167705140719,
  "radial_IAE_m_s": 0.6644215530598963,
  "signed_longitudinal_delta_m": 0.0037401779569578818,
  "tail_speed_mean_m_s": -0.00014829045182877148,
  "tail_speed_rms_m_s": 0.00015208963803991303,
  "tail_sensor_speed_mean_m_s": -0.0001929400148975309,
  "tail_fk_speed_mean_m_s": -0.00015907429105038474,
  "peak_tilt_rad": 0.1337976426944285,
  "peak_wheel_torque_nm": 2.221275806427002,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.5607694454688696,
  "final_integral_m_s": 0.5607694454688696,
  "elapsed_wall_s": 10.26503753499128
}
```
