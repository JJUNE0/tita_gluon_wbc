# tita_flash_sac_115632_883848_model_40000_v02_s911_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a4b5c15c3add7114e65d55cabbe505c0fffcd993df1b9162587e073cca97a891

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_40000_v02_s911_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_40000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 911,
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
  "checkpoint_sha256": "a4b5c15c3add7114e65d55cabbe505c0fffcd993df1b9162587e073cca97a891",
  "onnx_sha256": "4722a7e5dc4a1d465689d98943ba5c9a40a7d45a99344f923f067d1cfa90fcb6",
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
  "initial_physics_sha256": "a0c03b9d82435ab0b42ba90c67094e0519a05d4b24fcdcac8098f216bb90f593",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.021846415650708505,
  "max_drift_m": 0.039684201994060024,
  "radial_IAE_m_s": 6.706995827455685,
  "signed_longitudinal_delta_m": 0.02182534021616925,
  "tail_speed_mean_m_s": -4.769376737193084e-06,
  "tail_speed_rms_m_s": 4.771426512030602e-06,
  "tail_sensor_speed_mean_m_s": -4.6623674557844514e-06,
  "tail_fk_speed_mean_m_s": -2.923357408617492e-06,
  "peak_tilt_rad": 0.11350755028149773,
  "peak_wheel_torque_nm": 0.9394599199295044,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.23694472247722428,
  "final_integral_m_s": 0.23695009090638489,
  "elapsed_wall_s": 54.12017221096903
}
```
