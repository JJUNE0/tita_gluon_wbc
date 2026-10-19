# tita_flash_sac_115632_883848_model_55000_tau0.2_entry12

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: bb5591e26f71829becb4dab5c4e2effcd37054b9722c650dbf0e2ba993329aa7

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_55000_tau0.2_entry12",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_55000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 271,
    "estimator": "fk",
    "runtime": true,
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.2,
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
  "final_drift_m": 0.022268652054224913,
  "max_drift_m": 0.050118269604199836,
  "radial_IAE_m_s": 1.3939982984834247,
  "signed_longitudinal_delta_m": 0.02226325140270873,
  "tail_speed_mean_m_s": -1.8815796217126284e-05,
  "tail_speed_rms_m_s": 1.886731447021444e-05,
  "tail_sensor_speed_mean_m_s": -1.8244059086088334e-05,
  "tail_fk_speed_mean_m_s": -1.4917961695532025e-05,
  "peak_tilt_rad": 0.08957730764488736,
  "peak_wheel_torque_nm": 0.7944914698600769,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.2405553884224075,
  "final_integral_m_s": 0.24058665158333023,
  "elapsed_wall_s": 5.973442013957538
}
```
