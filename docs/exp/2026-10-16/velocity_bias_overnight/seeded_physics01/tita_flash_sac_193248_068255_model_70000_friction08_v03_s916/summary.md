# tita_flash_sac_193248_068255_model_70000_friction08_v03_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: e439f20c11a536f9853e4c13fe7127d3c2bbeba319ef7a99ce8cd3071d8c3d58

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_70000_friction08_v03_s916",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_70000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "friction": 0.8
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
  "checkpoint_sha256": "e439f20c11a536f9853e4c13fe7127d3c2bbeba319ef7a99ce8cd3071d8c3d58",
  "onnx_sha256": "69ed1a24755409f08a0de53dcb6bb767281a855b722e0c6e9fd6af7a63848138",
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
  "initial_physics_sha256": "c4f545a507a16c7c23f5159044fe8f1e0d117fa1b847496df258e16856be6d64",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.011997629345725186,
  "max_drift_m": 0.01243845886068225,
  "radial_IAE_m_s": 0.5712762350489751,
  "signed_longitudinal_delta_m": 0.01199752950676567,
  "tail_speed_mean_m_s": 8.223308566178867e-05,
  "tail_speed_rms_m_s": 8.223570103645457e-05,
  "tail_sensor_speed_mean_m_s": 8.217643481903688e-05,
  "tail_fk_speed_mean_m_s": 8.198467072487647e-05,
  "peak_tilt_rad": 0.0735598236615127,
  "peak_wheel_torque_nm": 0.06639150530099869,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0733984489337017,
  "final_integral_m_s": 0.0733984489337017,
  "elapsed_wall_s": 13.442164284002502
}
```
