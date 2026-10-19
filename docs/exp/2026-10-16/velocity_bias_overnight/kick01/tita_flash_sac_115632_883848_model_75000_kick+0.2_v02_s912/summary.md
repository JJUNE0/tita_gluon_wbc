# tita_flash_sac_115632_883848_model_75000_kick+0.2_v02_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 381e846e3ffb1d5a9ed629c02b55c9740ec3c5b089ca443f38b3d73b6abbd730

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_75000_kick+0.2_v02_s912",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_75000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 912,
    "estimator": "fk",
    "runtime": true,
    "kick": 0.2,
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
  "checkpoint_sha256": "381e846e3ffb1d5a9ed629c02b55c9740ec3c5b089ca443f38b3d73b6abbd730",
  "onnx_sha256": "2bd3f78d10bc3b7cc4e50272d0289147f13b0a62ac6730048ba653ae53f35114",
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
  "initial_physics_sha256": "976db50ecf9f15963a0a6fa6dbf1dc065a2548bb9a54cfe6d74271b7b7847419",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.0024275955466022533,
  "max_drift_m": 0.05580504003526565,
  "radial_IAE_m_s": 0.19185903986042285,
  "signed_longitudinal_delta_m": 0.002405160171900246,
  "tail_speed_mean_m_s": 9.768060647990946e-06,
  "tail_speed_rms_m_s": 9.829531440052465e-06,
  "tail_sensor_speed_mean_m_s": 9.802263478432174e-06,
  "tail_fk_speed_mean_m_s": 1.0463633906893236e-05,
  "peak_tilt_rad": 0.06667880603152687,
  "peak_wheel_torque_nm": 1.8185505867004395,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.004444792228143673,
  "final_integral_m_s": 0.004420011171363674,
  "elapsed_wall_s": 19.09581149497535
}
```
