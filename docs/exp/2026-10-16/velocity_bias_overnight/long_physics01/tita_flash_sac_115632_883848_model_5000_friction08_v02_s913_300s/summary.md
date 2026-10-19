# tita_flash_sac_115632_883848_model_5000_friction08_v02_s913_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: cc685c5efb437641f8ad47131a1b737aa37ee01ecbc81e3d5e5a21ebc1ddd90d

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_5000_friction08_v02_s913_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_5000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 913,
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
  "initial_physics_sha256": "c0fa3a831621244d92b2a89d915d88afff8850ae7288009dec0961a10ba6c445",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.042180901621014726,
  "max_drift_m": 0.08993103585687197,
  "radial_IAE_m_s": 13.33054733215295,
  "signed_longitudinal_delta_m": -0.04217316428951658,
  "tail_speed_mean_m_s": 8.399402275210629e-06,
  "tail_speed_rms_m_s": 0.0024995934540004536,
  "tail_sensor_speed_mean_m_s": -0.00019042985301899885,
  "tail_fk_speed_mean_m_s": 2.566748088649128e-05,
  "peak_tilt_rad": 0.18446940516654786,
  "peak_wheel_torque_nm": 3.2877838611602783,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.40232677192396715,
  "final_integral_m_s": -0.4039435866752361,
  "elapsed_wall_s": 84.38960475596832
}
```
