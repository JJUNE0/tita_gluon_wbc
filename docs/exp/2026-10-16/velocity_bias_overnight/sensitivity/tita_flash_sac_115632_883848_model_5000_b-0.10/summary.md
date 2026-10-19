# tita_flash_sac_115632_883848_model_5000_b-0.10

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: cc685c5efb437641f8ad47131a1b737aa37ee01ecbc81e3d5e5a21ebc1ddd90d

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_5000_b-0.10",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_5000",
    "duration": 40.0,
    "seed": 270,
    "warmup": 8.0,
    "law": {
      "mode": "constant",
      "bias": -0.1
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
  "final_drift_m": 6.108901492688913,
  "max_drift_m": 6.108901492688913,
  "radial_IAE_m_s": 123.11007725201657,
  "signed_longitudinal_delta_m": -5.990535698985358,
  "tail_speed_mean_m_s": -0.1525255900562748,
  "tail_speed_rms_m_s": 0.15385240852012286,
  "tail_sensor_speed_mean_m_s": -0.15215958695639623,
  "tail_fk_speed_mean_m_s": -0.15178731208375035,
  "peak_tilt_rad": 0.07264259816309182,
  "peak_wheel_torque_nm": 3.8614823818206787,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.1,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 4.801941631012596
}
```
