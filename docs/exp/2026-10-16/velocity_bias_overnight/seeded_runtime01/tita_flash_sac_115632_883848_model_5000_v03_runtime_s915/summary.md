# tita_flash_sac_115632_883848_model_5000_v03_runtime_s915

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: cc685c5efb437641f8ad47131a1b737aa37ee01ecbc81e3d5e5a21ebc1ddd90d

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_5000_v03_runtime_s915",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_5000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 915,
    "estimator": "fk",
    "runtime": true,
    "law": {
      "kp": 0.0,
      "ki": 4.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0,
      "seed_gain": 3.0
    },
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0",
    "controller_source_sha256": "6056e5bd50e0d84e7e554e390f2ede0726c82adf059af80911969c1286a3cded"
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
  "initial_physics_sha256": "750b8cb4997d587a4f1491c373224fee70bf03a6a0994bf1f9ecdd82a7620ccf",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.010284101794196863,
  "max_drift_m": 0.0954146497256441,
  "radial_IAE_m_s": 0.8802193398616774,
  "signed_longitudinal_delta_m": 0.010233641558503943,
  "tail_speed_mean_m_s": 9.494086330962485e-05,
  "tail_speed_rms_m_s": 0.0004447416902763714,
  "tail_sensor_speed_mean_m_s": 0.00010674549587126562,
  "tail_fk_speed_mean_m_s": 0.00010827641152720747,
  "peak_tilt_rad": 0.19611952705988167,
  "peak_wheel_torque_nm": 3.3480165004730225,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.45040922856871723,
  "final_integral_m_s": -0.45040922856871723,
  "elapsed_wall_s": 16.464514557039365
}
```
