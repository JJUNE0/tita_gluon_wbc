# tita_flash_sac_115632_883848_model_75000_kick-0.2_v02_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 381e846e3ffb1d5a9ed629c02b55c9740ec3c5b089ca443f38b3d73b6abbd730

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_75000_kick-0.2_v02_s912",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_75000",
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
  "initial_physics_sha256": "37fbf70b671387fbcd11a54bc66bef80fef54b39bb6bfc2832778f1b6cf1a28c",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.0003768413042527551,
  "max_drift_m": 0.10101880244915441,
  "radial_IAE_m_s": 0.1659552369069849,
  "signed_longitudinal_delta_m": -0.0003008905596244001,
  "tail_speed_mean_m_s": 1.1635017459481218e-05,
  "tail_speed_rms_m_s": 1.2064745225322322e-05,
  "tail_sensor_speed_mean_m_s": 1.1682343670738322e-05,
  "tail_fk_speed_mean_m_s": 1.2331952430847134e-05,
  "peak_tilt_rad": 0.13717367836608152,
  "peak_wheel_torque_nm": 1.6770944595336914,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.005112703241389748,
  "final_integral_m_s": 0.005074241957452412,
  "elapsed_wall_s": 17.768608169979416
}
```
