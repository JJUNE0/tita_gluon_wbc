# p001_tita_flash_sac_115632_883848_model_5000

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: cc685c5efb437641f8ad47131a1b737aa37ee01ecbc81e3d5e5a21ebc1ddd90d

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "p001_tita_flash_sac_115632_883848_model_5000",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_5000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 270,
    "law": {
      "kp": -2.0,
      "ki": 0.5,
      "tau": 0.5,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 1.0,
      "ramp": 1.5
    },
    "estimator": "fk"
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
  "duration_s": 60.0,
  "final_drift_m": 0.6974452992893231,
  "max_drift_m": 1.6669191775945142,
  "radial_IAE_m_s": 58.47729333848257,
  "signed_longitudinal_delta_m": -0.6934912156013673,
  "tail_speed_mean_m_s": 0.045302452671830494,
  "tail_speed_rms_m_s": 0.2022293416899296,
  "tail_sensor_speed_mean_m_s": 0.04638845892676469,
  "tail_fk_speed_mean_m_s": 0.045424866483341465,
  "peak_tilt_rad": 0.2531079502159792,
  "peak_wheel_torque_nm": 3.901136875152588,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0984475852147112,
  "final_integral_m_s": -0.3001792653308811,
  "elapsed_wall_s": 5.3451530619640835
}
```
