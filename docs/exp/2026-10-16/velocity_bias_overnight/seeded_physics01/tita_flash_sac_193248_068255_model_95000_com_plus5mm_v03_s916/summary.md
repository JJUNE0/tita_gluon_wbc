# tita_flash_sac_193248_068255_model_95000_com_plus5mm_v03_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a9ca81d693e2ee34f29bbb8746ae6c7a09f1a201d1d579d15a861fab83818441

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_95000_com_plus5mm_v03_s916",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_95000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "com": 0.005
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
  "checkpoint_sha256": "a9ca81d693e2ee34f29bbb8746ae6c7a09f1a201d1d579d15a861fab83818441",
  "onnx_sha256": "7e9315ab3ff8de6c69ba7599d9f20f2c432877c181d5c6228d4b55646de7b449",
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
  "initial_physics_sha256": "d5fede61dd3913e37a7b870c3381b6f2fdbf449b5f6351d065b0ca0f5e5109af",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.033310957134429796,
  "max_drift_m": 0.058640577314838564,
  "radial_IAE_m_s": 1.9563312942640958,
  "signed_longitudinal_delta_m": 0.03331019968808305,
  "tail_speed_mean_m_s": 2.7920797336915317e-05,
  "tail_speed_rms_m_s": 2.7929434233860894e-05,
  "tail_sensor_speed_mean_m_s": 2.8011976933231235e-05,
  "tail_fk_speed_mean_m_s": 2.7485312857070656e-05,
  "peak_tilt_rad": 0.07187049693290004,
  "peak_wheel_torque_nm": 0.3745056986808777,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.03632070067400909,
  "final_integral_m_s": -0.03632070067400909,
  "elapsed_wall_s": 10.431372936989646
}
```
