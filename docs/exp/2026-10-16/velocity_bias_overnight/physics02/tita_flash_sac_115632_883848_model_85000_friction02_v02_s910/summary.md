# tita_flash_sac_115632_883848_model_85000_friction02_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d1530cc4acd3186dfa88b59087ef850fd51f024ba7eba3252bc14a6549cc77d7

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_85000_friction02_v02_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_85000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "friction": 0.2
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
  "initial_physics_sha256": "139371344e21f51f2e471a0fc9999166635043836b7cf30e2b49c17f3385c4df",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.06210910545651917,
  "max_drift_m": 0.07348330146029111,
  "radial_IAE_m_s": 3.723375199019251,
  "signed_longitudinal_delta_m": 0.0621020873221143,
  "tail_speed_mean_m_s": -1.973254036188407e-07,
  "tail_speed_rms_m_s": 6.91683852431658e-07,
  "tail_sensor_speed_mean_m_s": -7.653059254997743e-06,
  "tail_fk_speed_mean_m_s": 4.29713406170259e-07,
  "peak_tilt_rad": 0.06531437755726333,
  "peak_wheel_torque_nm": 0.6057305335998535,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.6349545892220024,
  "final_integral_m_s": 0.6349544997184142,
  "elapsed_wall_s": 19.28464335401077
}
```
