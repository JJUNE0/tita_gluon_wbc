# p005_tita_flash_sac_115632_883848_model_5000

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: cc685c5efb437641f8ad47131a1b737aa37ee01ecbc81e3d5e5a21ebc1ddd90d

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "p005_tita_flash_sac_115632_883848_model_5000",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_5000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "physics": {},
    "kick": 0.0,
    "law": {
      "kp": 0.0,
      "ki": 2.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0,
      "seed_gain": 3.0
    }
  },
  "checkpoint_sha256": "cc685c5efb437641f8ad47131a1b737aa37ee01ecbc81e3d5e5a21ebc1ddd90d",
  "onnx_sha256": "4d80b373930fd59198e3fc588870f929175201ad8b748405f7e94231464a4d30",
  "input_columns": [
    "velocity_bias_m_s",
    "filtered_velocity_m_s",
    "integral_m_s"
  ],
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
  "initial_physics_sha256": "2f491c6051ffa90074a4c339f034d92dbbbe51740597259ac78cca40f029c33d",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.019286537326421223,
  "max_drift_m": 0.17441084559858722,
  "radial_IAE_m_s": 1.7455731804436034,
  "signed_longitudinal_delta_m": 0.01926783182679914,
  "tail_speed_mean_m_s": 0.00015867150718942887,
  "tail_speed_rms_m_s": 0.00016183110422977857,
  "tail_sensor_speed_mean_m_s": 0.00016783118964860147,
  "tail_fk_speed_mean_m_s": 0.00017195688624123,
  "peak_tilt_rad": 0.19853230536945143,
  "peak_wheel_torque_nm": 3.335507392883301,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.45165986786124224,
  "final_integral_m_s": -0.45165986786124224,
  "elapsed_wall_s": 4.657947952975519
}
```
