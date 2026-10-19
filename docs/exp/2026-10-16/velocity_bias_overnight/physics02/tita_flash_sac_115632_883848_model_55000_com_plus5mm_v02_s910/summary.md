# tita_flash_sac_115632_883848_model_55000_com_plus5mm_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: bb5591e26f71829becb4dab5c4e2effcd37054b9722c650dbf0e2ba993329aa7

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_55000_com_plus5mm_v02_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_55000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "com": 0.005
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
  "initial_physics_sha256": "00e82e9ffeb146ceec9c3be4e4f50b7e4f30979acb1f03da40f0f36f42531e74",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.026906788098088896,
  "max_drift_m": 0.05449295414839646,
  "radial_IAE_m_s": 1.6676061296546536,
  "signed_longitudinal_delta_m": 0.026903430537369988,
  "tail_speed_mean_m_s": -1.8709897309597698e-05,
  "tail_speed_rms_m_s": 1.8751312836825747e-05,
  "tail_sensor_speed_mean_m_s": -1.8033328501638823e-05,
  "tail_fk_speed_mean_m_s": -1.4964077876330082e-05,
  "peak_tilt_rad": 0.09145525569040847,
  "peak_wheel_torque_nm": 0.9236078262329102,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.2877937761723149,
  "final_integral_m_s": 0.28782647592849236,
  "elapsed_wall_s": 17.13398922799388
}
```
