# tita_flash_sac_115632_883848_model_80000_com_plus5mm_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 80677a4fd403aad22ca310d644998b9b9a686da481d6d95eaf8cc02aa67afadc

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_80000_com_plus5mm_baseline_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_80000",
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
  "initial_physics_sha256": "a70c89cfd2868b985651efc6559f5691ddecefae66af7b93784b6d89c63d0d38",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 12.91643577995035,
  "max_drift_m": 12.91643577995035,
  "radial_IAE_m_s": 380.97518509289114,
  "signed_longitudinal_delta_m": 12.849396576423878,
  "tail_speed_mean_m_s": 0.2204824886169537,
  "tail_speed_rms_m_s": 0.2204826815654654,
  "tail_sensor_speed_mean_m_s": 0.22000606976124415,
  "tail_fk_speed_mean_m_s": 0.22000516221603122,
  "peak_tilt_rad": 0.0880900312811368,
  "peak_wheel_torque_nm": 0.5248668193817139,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 14.566156837972812
}
```
