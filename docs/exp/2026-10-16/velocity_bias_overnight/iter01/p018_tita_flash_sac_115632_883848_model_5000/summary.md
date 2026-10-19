# p018_tita_flash_sac_115632_883848_model_5000

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: cc685c5efb437641f8ad47131a1b737aa37ee01ecbc81e3d5e5a21ebc1ddd90d

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "p018_tita_flash_sac_115632_883848_model_5000",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_5000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 270,
    "law": {
      "kp": 5.0,
      "ki": 0.5,
      "tau": 0.1,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 1.0,
      "ramp": 1.5
    },
    "estimator": "fk"
  },
  "checkpoint_sha256": "cc685c5efb437641f8ad47131a1b737aa37ee01ecbc81e3d5e5a21ebc1ddd90d",
  "onnx_sha256": "4d80b373930fd59198e3fc588870f929175201ad8b748405f7e94231464a4d30",
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
  "initial_physics_sha256": "a14405f43198ecdfbefad595d127e0ed04bbd8d9cfddc7aaa119e9f369851b61",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 1.1588944172711089,
  "max_drift_m": 1.5428015215093422,
  "radial_IAE_m_s": 68.58711248452894,
  "signed_longitudinal_delta_m": -1.1575145961201794,
  "tail_speed_mean_m_s": 0.01753512563053709,
  "tail_speed_rms_m_s": 0.024672259219728394,
  "tail_sensor_speed_mean_m_s": 0.01753356352076682,
  "tail_fk_speed_mean_m_s": 0.017570084931816873,
  "peak_tilt_rad": 0.17161550360672173,
  "peak_wheel_torque_nm": 4.2145209312438965,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.5031803818931638,
  "final_integral_m_s": -0.5750682050824338,
  "elapsed_wall_s": 4.687084600969683
}
```
