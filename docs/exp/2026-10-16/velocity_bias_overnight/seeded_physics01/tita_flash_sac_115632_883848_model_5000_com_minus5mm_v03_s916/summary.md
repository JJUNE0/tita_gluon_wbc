# tita_flash_sac_115632_883848_model_5000_com_minus5mm_v03_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: cc685c5efb437641f8ad47131a1b737aa37ee01ecbc81e3d5e5a21ebc1ddd90d

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_5000_com_minus5mm_v03_s916",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_5000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "com": -0.005
    },
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
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
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
  "initial_physics_sha256": "7c0faf89760deeecf0199a742f4dc9111c0f284b116c5d0d9d6006df57efd7d8",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.025373201293046235,
  "max_drift_m": 0.09387988621515747,
  "radial_IAE_m_s": 1.7553899601894032,
  "signed_longitudinal_delta_m": 0.02537319961271658,
  "tail_speed_mean_m_s": 6.944957037469213e-05,
  "tail_speed_rms_m_s": 0.0003331239968733313,
  "tail_sensor_speed_mean_m_s": 7.907410507168411e-05,
  "tail_fk_speed_mean_m_s": 8.016049264026802e-05,
  "peak_tilt_rad": 0.19688918663004973,
  "peak_wheel_torque_nm": 3.4150571823120117,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.4974972467255352,
  "final_integral_m_s": -0.4974972467255352,
  "elapsed_wall_s": 10.110000633983873
}
```
