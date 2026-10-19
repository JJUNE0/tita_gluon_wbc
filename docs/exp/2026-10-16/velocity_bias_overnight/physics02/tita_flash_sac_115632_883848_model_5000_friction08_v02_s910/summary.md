# tita_flash_sac_115632_883848_model_5000_friction08_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: cc685c5efb437641f8ad47131a1b737aa37ee01ecbc81e3d5e5a21ebc1ddd90d

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_5000_friction08_v02_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_5000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "friction": 0.8
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
  "initial_physics_sha256": "20858b84d804ab31e1cd334d0b38917005a7e867f598005a1abb5dd9302de7a4",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.045290669459508937,
  "max_drift_m": 0.08990646968974586,
  "radial_IAE_m_s": 2.8494147783870405,
  "signed_longitudinal_delta_m": -0.04524576641220289,
  "tail_speed_mean_m_s": 1.282598830951871e-05,
  "tail_speed_rms_m_s": 0.0001244949588386563,
  "tail_sensor_speed_mean_m_s": 1.7576890271880453e-05,
  "tail_fk_speed_mean_m_s": 2.2842660846581727e-05,
  "peak_tilt_rad": 0.18437971925837293,
  "peak_wheel_torque_nm": 3.2900469303131104,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.4439314007964162,
  "final_integral_m_s": -0.4440194656164201,
  "elapsed_wall_s": 16.88060613896232
}
```
