# tita_flash_sac_115632_883848_model_40000_friction02_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a4b5c15c3add7114e65d55cabbe505c0fffcd993df1b9162587e073cca97a891

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_40000_friction02_v02_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_40000",
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
  "initial_physics_sha256": "642ebc5b304ecc03661297ec2228d6e312b4187624a45dc961d516ea881eb927",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.02708850676974108,
  "max_drift_m": 0.03966595936460088,
  "radial_IAE_m_s": 1.358701257796469,
  "signed_longitudinal_delta_m": 0.025228777790614627,
  "tail_speed_mean_m_s": -0.00010981395799698195,
  "tail_speed_rms_m_s": 0.00010981397293257457,
  "tail_sensor_speed_mean_m_s": -3.07514824462598e-05,
  "tail_fk_speed_mean_m_s": -1.1521152314525146e-07,
  "peak_tilt_rad": 0.10852838356225525,
  "peak_wheel_torque_nm": 0.9156373739242554,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.21666798595856704,
  "final_integral_m_s": 0.21666804791046843,
  "elapsed_wall_s": 12.862657557998318
}
```
