# tita_flash_sac_115632_883848_model_85000_com_plus5mm_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d1530cc4acd3186dfa88b59087ef850fd51f024ba7eba3252bc14a6549cc77d7

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_85000_com_plus5mm_baseline_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_85000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "com": 0.005
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
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
  "initial_physics_sha256": "cb911041b2851835a2c17b37fb8f34943a889c2a398006c9d72d82fdd4099ffe",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 8.294214985363777,
  "max_drift_m": 8.294214985363777,
  "radial_IAE_m_s": 244.6559220147589,
  "signed_longitudinal_delta_m": 8.259463500721333,
  "tail_speed_mean_m_s": 0.14226813657607884,
  "tail_speed_rms_m_s": 0.1422697700968699,
  "tail_sensor_speed_mean_m_s": 0.14196058569476358,
  "tail_fk_speed_mean_m_s": 0.14196073186414565,
  "peak_tilt_rad": 0.06662884587814388,
  "peak_wheel_torque_nm": 0.1375618577003479,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 11.752812966005877
}
```
