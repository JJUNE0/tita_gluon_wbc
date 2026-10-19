# tita_flash_sac_115632_883848_model_85000_v02_s911_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d1530cc4acd3186dfa88b59087ef850fd51f024ba7eba3252bc14a6549cc77d7

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_85000_v02_s911_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_85000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 911,
    "estimator": "fk",
    "runtime": true,
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
  "initial_physics_sha256": "f4cf662d676d1d1388509ca848ff299dbeb51b25bd94fc13372e0ccf234f7659",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.06357180845723488,
  "max_drift_m": 0.0658132977405815,
  "radial_IAE_m_s": 17.832226320573618,
  "signed_longitudinal_delta_m": 0.06357146770255505,
  "tail_speed_mean_m_s": 3.137632766952638e-05,
  "tail_speed_rms_m_s": 3.1376420394109795e-05,
  "tail_sensor_speed_mean_m_s": 3.0721105661320784e-05,
  "tail_fk_speed_mean_m_s": 3.191270355642821e-05,
  "peak_tilt_rad": 0.06545748155423148,
  "peak_wheel_torque_nm": 0.4996802806854248,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.64553639894583,
  "final_integral_m_s": 0.6454728316955411,
  "elapsed_wall_s": 71.62385276303394
}
```
