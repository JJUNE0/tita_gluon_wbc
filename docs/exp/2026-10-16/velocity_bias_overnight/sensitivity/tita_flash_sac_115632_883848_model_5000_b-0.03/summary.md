# tita_flash_sac_115632_883848_model_5000_b-0.03

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: cc685c5efb437641f8ad47131a1b737aa37ee01ecbc81e3d5e5a21ebc1ddd90d

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_5000_b-0.03",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_5000",
    "duration": 40.0,
    "seed": 270,
    "warmup": 8.0,
    "law": {
      "mode": "constant",
      "bias": -0.03
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
  "initial_physics_sha256": "a14405f43198ecdfbefad595d127e0ed04bbd8d9cfddc7aaa119e9f369851b61",
  "complete": true,
  "failure": [],
  "duration_s": 40.0,
  "final_drift_m": 6.563132419160836,
  "max_drift_m": 6.563132419160836,
  "radial_IAE_m_s": 132.01736299625955,
  "signed_longitudinal_delta_m": -6.421175846343623,
  "tail_speed_mean_m_s": -0.1643476154633596,
  "tail_speed_rms_m_s": 0.16560827869729725,
  "tail_sensor_speed_mean_m_s": -0.16381880445563665,
  "tail_fk_speed_mean_m_s": -0.16355572938943017,
  "peak_tilt_rad": 0.07278454133606127,
  "peak_wheel_torque_nm": 3.8840341567993164,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.03,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 4.65036147198407
}
```
