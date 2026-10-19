# tita_flash_sac_115632_883848_model_85000_friction08_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d1530cc4acd3186dfa88b59087ef850fd51f024ba7eba3252bc14a6549cc77d7

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_85000_friction08_baseline_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_85000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "friction": 0.8
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
  "initial_physics_sha256": "a53e9d728130568d39dd2c2c2615367be8f863952ed7e585251ee807615b9264",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 7.335068218311554,
  "max_drift_m": 7.335068218311554,
  "radial_IAE_m_s": 215.88819622004792,
  "signed_longitudinal_delta_m": 7.290571421889567,
  "tail_speed_mean_m_s": 0.1263593650546592,
  "tail_speed_rms_m_s": 0.12636177763355316,
  "tail_sensor_speed_mean_m_s": 0.1260865810763324,
  "tail_fk_speed_mean_m_s": 0.12608684025249156,
  "peak_tilt_rad": 0.06759715089069673,
  "peak_wheel_torque_nm": 0.14721214771270752,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 12.212959714001045
}
```
