# tita_flash_sac_115632_883848_model_55000_tau0.05_entry12

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: bb5591e26f71829becb4dab5c4e2effcd37054b9722c650dbf0e2ba993329aa7

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_55000_tau0.05_entry12",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_55000",
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
  "final_drift_m": 0.022271390201419897,
  "max_drift_m": 0.04328926537085299,
  "radial_IAE_m_s": 1.3906710671483336,
  "signed_longitudinal_delta_m": 0.022266088399592817,
  "tail_speed_mean_m_s": -1.8797661914882456e-05,
  "tail_speed_rms_m_s": 1.8845146993574475e-05,
  "tail_sensor_speed_mean_m_s": -1.8204963875054134e-05,
  "tail_fk_speed_mean_m_s": -1.4878232205863665e-05,
  "peak_tilt_rad": 0.08956801417971416,
  "peak_wheel_torque_nm": 1.0171663761138916,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.24058002140755144,
  "final_integral_m_s": 0.24061132710715682,
  "elapsed_wall_s": 5.968926573987119
}
```
