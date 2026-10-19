# tita_flash_sac_193248_068255_model_65000_v03_s918_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 950b5958dfae8344a2f3cfbf5d26f83d6cac60eaaf404962bb8ea0b163f7244e

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_65000_v03_s918_300s",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_65000",
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
  "checkpoint_sha256": "950b5958dfae8344a2f3cfbf5d26f83d6cac60eaaf404962bb8ea0b163f7244e",
  "onnx_sha256": "a1f326d5979e91ea8e5b962f09eb3e8da4d889ac9902563756ff9179048872c8",
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
  "initial_physics_sha256": "1e74c6c3a68aee300ca75360d8a2240d8d5a23121f2febdab5ddc68677551f26",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.01263281960897124,
  "max_drift_m": 0.03423393673471956,
  "radial_IAE_m_s": 4.478418764776978,
  "signed_longitudinal_delta_m": -0.012554456966966318,
  "tail_speed_mean_m_s": 8.998359248507213e-06,
  "tail_speed_rms_m_s": 9.000348567214292e-06,
  "tail_sensor_speed_mean_m_s": 8.925549114396275e-06,
  "tail_fk_speed_mean_m_s": 9.86179254767235e-06,
  "peak_tilt_rad": 0.04857346034463905,
  "peak_wheel_torque_nm": 0.2352183312177658,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.17108534903851988,
  "final_integral_m_s": -0.17108534903851988,
  "elapsed_wall_s": 23.335605612024665
}
```
