# p020_tita_flash_sac_115632_883848_model_5000

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: cc685c5efb437641f8ad47131a1b737aa37ee01ecbc81e3d5e5a21ebc1ddd90d

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "p020_tita_flash_sac_115632_883848_model_5000",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_5000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 270,
    "law": {
      "kp": 5.0,
      "ki": 2.0,
      "tau": 0.1,
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
  "final_drift_m": 0.23190726035165693,
  "max_drift_m": 0.3970695882167582,
  "radial_IAE_m_s": 15.425864357929338,
  "signed_longitudinal_delta_m": -0.2319072514926108,
  "tail_speed_mean_m_s": 0.00011584492692537639,
  "tail_speed_rms_m_s": 0.00011716828483819565,
  "tail_sensor_speed_mean_m_s": 0.00012816113621170346,
  "tail_fk_speed_mean_m_s": 0.0001338671214126087,
  "peak_tilt_rad": 0.17476888484156916,
  "peak_wheel_torque_nm": 4.022213935852051,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.4633526221028098,
  "final_integral_m_s": -0.4642585065859495,
  "elapsed_wall_s": 4.786794924992137
}
```
