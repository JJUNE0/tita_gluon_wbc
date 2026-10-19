# tita_flash_sac_115632_883848_model_95000_v02_s911_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 7fc976ceb0b69090d3baf26399d36e566e21da7bf1a3f935bf0a1bc7b29a5d82

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_95000_v02_s911_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_95000",
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
  "checkpoint_sha256": "7fc976ceb0b69090d3baf26399d36e566e21da7bf1a3f935bf0a1bc7b29a5d82",
  "onnx_sha256": "1a45e6567675d4dfc1a738bbe430e52a4f2a2cab73c2c908c46928d22bd54530",
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
  "initial_physics_sha256": "856613d9d9d1c3ad9f7f87d43714ce6a4ae03d77e3ef82b90e638d1c1b6afffd",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.040728447111570636,
  "max_drift_m": 0.040728447111570636,
  "radial_IAE_m_s": 6.330446992980347,
  "signed_longitudinal_delta_m": 0.03995691723914621,
  "tail_speed_mean_m_s": 0.0001148769116294256,
  "tail_speed_rms_m_s": 0.00011488119022907398,
  "tail_sensor_speed_mean_m_s": 0.00011398626031391405,
  "tail_fk_speed_mean_m_s": 0.000114862124621037,
  "peak_tilt_rad": 0.06108813971321858,
  "peak_wheel_torque_nm": 0.1859056055545807,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.4093455968154364,
  "final_integral_m_s": 0.40911925783317643,
  "elapsed_wall_s": 77.58251954696607
}
```
