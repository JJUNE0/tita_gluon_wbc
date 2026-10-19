# tita_flash_sac_115632_883848_model_55000_friction02_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: bb5591e26f71829becb4dab5c4e2effcd37054b9722c650dbf0e2ba993329aa7

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_55000_friction02_v02_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_55000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "friction": 0.2
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
  "initial_physics_sha256": "b529b928de2d71af02109c000e95c58120dcffe89c0f5b5ad3f679ffc5c0b056",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.016788532412747262,
  "max_drift_m": 0.038508165765652545,
  "radial_IAE_m_s": 0.911860104177556,
  "signed_longitudinal_delta_m": 0.016136373600923334,
  "tail_speed_mean_m_s": -1.4298042002158876e-05,
  "tail_speed_rms_m_s": 3.469233447086806e-05,
  "tail_sensor_speed_mean_m_s": -5.047291163989444e-05,
  "tail_fk_speed_mean_m_s": -2.3554763178365093e-05,
  "peak_tilt_rad": 0.08308769627965829,
  "peak_wheel_torque_nm": 0.7274582386016846,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.17512112724564693,
  "final_integral_m_s": 0.175305449335841,
  "elapsed_wall_s": 19.872612885024864
}
```
