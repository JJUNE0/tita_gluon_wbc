# tita_flash_sac_193248_068255_model_70000_s271

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: e439f20c11a536f9853e4c13fe7127d3c2bbeba319ef7a99ce8cd3071d8c3d58

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_70000_s271",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_70000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 271,
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.05,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
    },
    "estimator": "fk"
  },
  "checkpoint_sha256": "e439f20c11a536f9853e4c13fe7127d3c2bbeba319ef7a99ce8cd3071d8c3d58",
  "onnx_sha256": "69ed1a24755409f08a0de53dcb6bb767281a855b722e0c6e9fd6af7a63848138",
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
  "initial_physics_sha256": "4efe6c997ecfbcc4f991be32cc756130b28f5790637a57f5d7d67744acf30210",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.008353985868997339,
  "max_drift_m": 0.018057901792102277,
  "radial_IAE_m_s": 0.4613380706139435,
  "signed_longitudinal_delta_m": 0.008353791455083524,
  "tail_speed_mean_m_s": 2.392959746036107e-05,
  "tail_speed_rms_m_s": 2.3931044471277635e-05,
  "tail_sensor_speed_mean_m_s": 2.4010376864859546e-05,
  "tail_fk_speed_mean_m_s": 2.372845066094362e-05,
  "peak_tilt_rad": 0.07881177074995938,
  "peak_wheel_torque_nm": 0.35633087158203125,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.08889980748785636,
  "final_integral_m_s": 0.08885336369527068,
  "elapsed_wall_s": 4.440755726012867
}
```
