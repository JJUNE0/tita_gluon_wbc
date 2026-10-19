# p006_tita_flash_sac_115632_883848_model_5000

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: cc685c5efb437641f8ad47131a1b737aa37ee01ecbc81e3d5e5a21ebc1ddd90d

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "p006_tita_flash_sac_115632_883848_model_5000",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_5000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "physics": {},
    "kick": 0.0,
    "law": {
      "kp": 0.0,
      "ki": 0.5,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0,
      "seed_gain": 4.0
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
  "final_drift_m": 0.39516075211513274,
  "max_drift_m": 0.39516075211513274,
  "radial_IAE_m_s": 19.61505976734729,
  "signed_longitudinal_delta_m": 0.39463128624418586,
  "tail_speed_mean_m_s": 0.0006986844681743571,
  "tail_speed_rms_m_s": 0.0007043414191757003,
  "tail_sensor_speed_mean_m_s": 0.0007102961357358902,
  "tail_fk_speed_mean_m_s": 0.0007148231903448579,
  "peak_tilt_rad": 0.19556864037926092,
  "peak_wheel_torque_nm": 3.3752214908599854,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.4589645877045976,
  "final_integral_m_s": -0.4589645877045976,
  "elapsed_wall_s": 4.595956398989074
}
```
