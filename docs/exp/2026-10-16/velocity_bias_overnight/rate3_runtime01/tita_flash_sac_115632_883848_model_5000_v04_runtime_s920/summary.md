# tita_flash_sac_115632_883848_model_5000_v04_runtime_s920

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: cc685c5efb437641f8ad47131a1b737aa37ee01ecbc81e3d5e5a21ebc1ddd90d

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_5000_v04_runtime_s920",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_5000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 920,
    "estimator": "fk",
    "runtime": true,
    "law": {
      "kp": 0.0,
      "ki": 4.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 3.0,
      "seed_gain": 3.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f",
    "controller_source_sha256": "4e549f65ed2d2f9b18e668a01f29676c85b4cabf11d295c503fd83ad71b2171f"
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
  "initial_physics_sha256": "cd0cbdd7dcc4a2f407c1932fde5df2b7ca9be637b51aa60b930c6c2b899758c2",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.009566944759681888,
  "max_drift_m": 0.09574709054376448,
  "radial_IAE_m_s": 0.8664510570261903,
  "signed_longitudinal_delta_m": 0.009503259963392345,
  "tail_speed_mean_m_s": 0.00010983100022383278,
  "tail_speed_rms_m_s": 0.001648347285642585,
  "tail_sensor_speed_mean_m_s": 0.00012149220776461165,
  "tail_fk_speed_mean_m_s": 0.00012243250929457237,
  "peak_tilt_rad": 0.19657148808617886,
  "peak_wheel_torque_nm": 3.324355125427246,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.44895687625894926,
  "final_integral_m_s": -0.44895687625894926,
  "elapsed_wall_s": 14.404907541000284
}
```
