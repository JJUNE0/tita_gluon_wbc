# tita_flash_sac_115632_883848_model_30000_v03_s918_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: ecff0682f7eaeee36f7e64c94170672ae7e912f30c8502429bab1e017f7ca17a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_30000_v03_s918_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_30000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 918,
    "estimator": "fk",
    "guarded": true,
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
  "checkpoint_sha256": "ecff0682f7eaeee36f7e64c94170672ae7e912f30c8502429bab1e017f7ca17a",
  "onnx_sha256": "e68dce44a40c95e38733c80c73616e51e12114a29c11f53063c1d02eb989061e",
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
  "initial_physics_sha256": "506fdb554add296c9312f02d131fa8cfcb1b5c1f3a9ac64f7ebe12266176398b",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.05228398621932577,
  "max_drift_m": 0.11392463522675975,
  "radial_IAE_m_s": 10.200506978008939,
  "signed_longitudinal_delta_m": -0.05223908744412605,
  "tail_speed_mean_m_s": -0.0001379370125469896,
  "tail_speed_rms_m_s": 0.0001380530179799228,
  "tail_sensor_speed_mean_m_s": -0.00013801090110628704,
  "tail_fk_speed_mean_m_s": -0.00013743144699313048,
  "peak_tilt_rad": 0.1271062016011857,
  "peak_wheel_torque_nm": 0.7961481213569641,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.435605367528186,
  "final_integral_m_s": 0.435605367528186,
  "elapsed_wall_s": 56.231226978008635
}
```
