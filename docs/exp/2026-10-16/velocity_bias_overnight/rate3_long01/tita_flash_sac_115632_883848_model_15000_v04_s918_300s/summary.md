# tita_flash_sac_115632_883848_model_15000_v04_s918_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 966f7a286b3139a7c633828fa375c6eeb4645d5eed73f64ed986c1c72dc72003

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_15000_v04_s918_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_15000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 918,
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
  "checkpoint_sha256": "966f7a286b3139a7c633828fa375c6eeb4645d5eed73f64ed986c1c72dc72003",
  "onnx_sha256": "1fec00b7bc7eebbc5b6decf23ac6f29b8799c5cf64ff1dee51c1ba762cf013ed",
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
  "initial_physics_sha256": "7a5112a26c976ba7896195ac5c36c977a0ee0588199db23aa46fe33a8c870fe2",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.027198909161072878,
  "max_drift_m": 0.052409688809251946,
  "radial_IAE_m_s": 8.764339942792784,
  "signed_longitudinal_delta_m": -0.027094711993077093,
  "tail_speed_mean_m_s": 8.324171986353102e-06,
  "tail_speed_rms_m_s": 8.333207328287167e-06,
  "tail_sensor_speed_mean_m_s": 8.48361637593667e-06,
  "tail_fk_speed_mean_m_s": 8.719773811325904e-06,
  "peak_tilt_rad": 0.12343990055493981,
  "peak_wheel_torque_nm": 2.5723798274993896,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.35509973832484276,
  "final_integral_m_s": -0.35509973832484276,
  "elapsed_wall_s": 79.47148095397279
}
```
