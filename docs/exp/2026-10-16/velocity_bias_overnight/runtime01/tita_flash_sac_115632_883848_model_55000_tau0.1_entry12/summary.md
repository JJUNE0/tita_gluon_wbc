# tita_flash_sac_115632_883848_model_55000_tau0.1_entry12

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: bb5591e26f71829becb4dab5c4e2effcd37054b9722c650dbf0e2ba993329aa7

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_55000_tau0.1_entry12",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_55000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 271,
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
  "checkpoint_sha256": "bb5591e26f71829becb4dab5c4e2effcd37054b9722c650dbf0e2ba993329aa7",
  "onnx_sha256": "8e2044f08b14f84be2b6152fb6085b58a0f6e377394a8fa0f7c69ebac1c08718",
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
  "initial_physics_sha256": "d5fffe21f3af240e8ef16e367cc9e89439d10afbf8e466733205cd85a8551fd8",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.022270589688134352,
  "max_drift_m": 0.045210374327367554,
  "radial_IAE_m_s": 1.391347492049381,
  "signed_longitudinal_delta_m": 0.022265156071456328,
  "tail_speed_mean_m_s": -1.880582254890861e-05,
  "tail_speed_rms_m_s": 1.885417910087668e-05,
  "tail_sensor_speed_mean_m_s": -1.821864490764202e-05,
  "tail_fk_speed_mean_m_s": -1.489156565809791e-05,
  "peak_tilt_rad": 0.08957047923333938,
  "peak_wheel_torque_nm": 0.9879575967788696,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.24057423459723284,
  "final_integral_m_s": 0.24060558593721293,
  "elapsed_wall_s": 5.969796850986313
}
```
