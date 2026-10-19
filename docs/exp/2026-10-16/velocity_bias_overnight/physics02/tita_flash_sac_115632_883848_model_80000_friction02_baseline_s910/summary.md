# tita_flash_sac_115632_883848_model_80000_friction02_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 80677a4fd403aad22ca310d644998b9b9a686da481d6d95eaf8cc02aa67afadc

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_80000_friction02_baseline_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_80000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "friction": 0.2
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "80677a4fd403aad22ca310d644998b9b9a686da481d6d95eaf8cc02aa67afadc",
  "onnx_sha256": "c7a83d6c9814cc6aa8357e4b0215d65d880dd6b756de2de920967396e901c93b",
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
  "initial_physics_sha256": "e66087af55f394adfc1cea35a61c1648b6f45160773693b27e280139f270d9ca",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 2.2499032695404613,
  "max_drift_m": 4.508090827579987,
  "radial_IAE_m_s": 193.82937123529933,
  "signed_longitudinal_delta_m": -2.1742059518697223,
  "tail_speed_mean_m_s": 0.20368783490561718,
  "tail_speed_rms_m_s": 0.20368813230324945,
  "tail_sensor_speed_mean_m_s": 0.20330677319827295,
  "tail_fk_speed_mean_m_s": 0.20336559098028836,
  "peak_tilt_rad": 0.08547088380526291,
  "peak_wheel_torque_nm": 0.2265458106994629,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 14.262046099000145
}
```
