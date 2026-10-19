# tita_flash_sac_115632_883848_model_40000_kick-0.2_v02_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a4b5c15c3add7114e65d55cabbe505c0fffcd993df1b9162587e073cca97a891

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_40000_kick-0.2_v02_s912",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_40000",
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
  "initial_physics_sha256": "8cffe3988f1e3662dfe1b4f5103512e3e3dcf352761124be83e74c0799e673fc",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.02085483492999066,
  "max_drift_m": 0.033080606909735126,
  "radial_IAE_m_s": 1.2253970894217663,
  "signed_longitudinal_delta_m": 0.0208515510728825,
  "tail_speed_mean_m_s": 1.655810142235423e-05,
  "tail_speed_rms_m_s": 1.6622000896494705e-05,
  "tail_sensor_speed_mean_m_s": 1.6043773729619842e-05,
  "tail_fk_speed_mean_m_s": 1.839591167413748e-05,
  "peak_tilt_rad": 0.12999869431296118,
  "peak_wheel_torque_nm": 1.8305906057357788,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.23741462024578214,
  "final_integral_m_s": 0.23737293060338108,
  "elapsed_wall_s": 12.7680716420291
}
```
