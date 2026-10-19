# tita_flash_sac_115632_883848_model_90000_friction08_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 4930085834f72c133d65563169762514342959361a6d71630216f5f608b0531f

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_90000_friction08_baseline_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_90000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "friction": 0.8
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "4930085834f72c133d65563169762514342959361a6d71630216f5f608b0531f",
  "onnx_sha256": "1d6ffa5d91a15cf74e2abf755c367c1fb151f6e3c740618a6e1fb2fbf28f9379",
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
  "initial_physics_sha256": "49fa6dfc847339872b2a144c5a0c3b442b40e952b01ceea29751089fc1cd6db1",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 6.686943338001166,
  "max_drift_m": 6.686943338001166,
  "radial_IAE_m_s": 198.7680448020087,
  "signed_longitudinal_delta_m": 6.6861601426939705,
  "tail_speed_mean_m_s": 0.11315982875473643,
  "tail_speed_rms_m_s": 0.11316018855170298,
  "tail_sensor_speed_mean_m_s": 0.11291481535751369,
  "tail_fk_speed_mean_m_s": 0.112913160759424,
  "peak_tilt_rad": 0.0720648813958098,
  "peak_wheel_torque_nm": 0.17045313119888306,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 11.99788008100586
}
```
