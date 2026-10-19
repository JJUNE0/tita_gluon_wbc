# tita_flash_sac_115632_883848_model_5000_kick+0.2_v02_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: cc685c5efb437641f8ad47131a1b737aa37ee01ecbc81e3d5e5a21ebc1ddd90d

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_5000_kick+0.2_v02_s912",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_5000",
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
  "checkpoint_sha256": "cc685c5efb437641f8ad47131a1b737aa37ee01ecbc81e3d5e5a21ebc1ddd90d",
  "onnx_sha256": "4d80b373930fd59198e3fc588870f929175201ad8b748405f7e94231464a4d30",
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
  "initial_physics_sha256": "ba490dd767589b7743c8287078a7b4834ef2513cc1405fbd05d4f70782e02b34",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.044793665665131946,
  "max_drift_m": 0.08715233841631277,
  "radial_IAE_m_s": 2.814346767283263,
  "signed_longitudinal_delta_m": -0.04475476202669035,
  "tail_speed_mean_m_s": 1.9807628340487458e-05,
  "tail_speed_rms_m_s": 0.0005686979952444479,
  "tail_sensor_speed_mean_m_s": 2.6720188321327098e-05,
  "tail_fk_speed_mean_m_s": 3.196349662894578e-05,
  "peak_tilt_rad": 0.18204051640544128,
  "peak_wheel_torque_nm": 3.416499376296997,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.49334586668542985,
  "final_integral_m_s": -0.49333291420022213,
  "elapsed_wall_s": 22.89510868198704
}
```
