# tita_flash_sac_193248_068255_model_50000_tau0.05_entry12

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 948c108cb4740ede74b9c33fdca02f3a0bc4ae70aeb862e20f90c841243b1087

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_50000_tau0.05_entry12",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_50000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 271,
    "estimator": "fk",
    "runtime": true,
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.05,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
    }
  },
  "checkpoint_sha256": "948c108cb4740ede74b9c33fdca02f3a0bc4ae70aeb862e20f90c841243b1087",
  "onnx_sha256": "9edc5ad830f2e0f0d88dcb9bd8a21a023d3cdd754ce2e54339650dc66d2bb1c4",
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
  "initial_physics_sha256": "1315e3204cfff9981202a4e9ceff7e951e07ac26a8155bfa3bf7762d31643676",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.0689937567791958,
  "max_drift_m": 0.0689937567791958,
  "radial_IAE_m_s": 4.023395191254746,
  "signed_longitudinal_delta_m": 0.06899228443457808,
  "tail_speed_mean_m_s": 2.1070499697318767e-05,
  "tail_speed_rms_m_s": 2.118868454738943e-05,
  "tail_sensor_speed_mean_m_s": 2.0950534398387064e-05,
  "tail_fk_speed_mean_m_s": 2.2016145907680514e-05,
  "peak_tilt_rad": 0.05075974227042401,
  "peak_wheel_torque_nm": 0.7503114938735962,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.6973926538974394,
  "final_integral_m_s": 0.6973520713693862,
  "elapsed_wall_s": 8.977450462989509
}
```
