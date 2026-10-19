# tita_flash_sac_115632_883848_model_55000_mass130_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: bb5591e26f71829becb4dab5c4e2effcd37054b9722c650dbf0e2ba993329aa7

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_55000_mass130_v02_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_55000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "mass": 1.3
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
  "initial_physics_sha256": "235115fa60c96139deb8606d083d86461a60de504ff0f8fc795f697c1a57a519",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.012025697067611562,
  "max_drift_m": 0.020852594538579742,
  "radial_IAE_m_s": 0.7106562123117142,
  "signed_longitudinal_delta_m": -0.012025059832904009,
  "tail_speed_mean_m_s": -8.130311756008741e-06,
  "tail_speed_rms_m_s": 8.137133311035683e-06,
  "tail_sensor_speed_mean_m_s": -7.673241018150885e-06,
  "tail_fk_speed_mean_m_s": -7.236688597797865e-06,
  "peak_tilt_rad": 0.1500078215606413,
  "peak_wheel_torque_nm": 0.7537133693695068,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.12767301504746265,
  "final_integral_m_s": -0.12765964013031317,
  "elapsed_wall_s": 16.372213265975006
}
```
