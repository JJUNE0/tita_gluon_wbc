# tita_flash_sac_115632_883848_model_55000_kick-0.2_v02_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: bb5591e26f71829becb4dab5c4e2effcd37054b9722c650dbf0e2ba993329aa7

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_55000_kick-0.2_v02_s912",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_55000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 912,
    "estimator": "fk",
    "runtime": true,
    "kick": -0.2,
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
  "initial_physics_sha256": "cda5e9551ff0d97bf1bad8beb0f481eb566802d90c0fbf35b2762bddc61612bd",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.020901497509815715,
  "max_drift_m": 0.03689405169472709,
  "radial_IAE_m_s": 1.2967213795405703,
  "signed_longitudinal_delta_m": 0.020863613586458118,
  "tail_speed_mean_m_s": -1.880244543565913e-05,
  "tail_speed_rms_m_s": 1.8850596844913438e-05,
  "tail_sensor_speed_mean_m_s": -1.825403447216688e-05,
  "tail_fk_speed_mean_m_s": -1.4928559187037966e-05,
  "peak_tilt_rad": 0.10083460382994214,
  "peak_wheel_torque_nm": 1.888175129890442,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.24407974853997738,
  "final_integral_m_s": 0.24411103686228058,
  "elapsed_wall_s": 15.207563401025254
}
```
