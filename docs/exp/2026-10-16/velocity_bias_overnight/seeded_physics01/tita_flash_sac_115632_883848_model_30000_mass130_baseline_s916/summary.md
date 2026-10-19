# tita_flash_sac_115632_883848_model_30000_mass130_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: ecff0682f7eaeee36f7e64c94170672ae7e912f30c8502429bab1e017f7ca17a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_30000_mass130_baseline_s916",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_30000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "mass": 1.3
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
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
  "initial_physics_sha256": "60b2056bf1d059f43e49da7ed5838fc9846a1e5a1eb5927f8dca8768e782919f",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 10.76168896624531,
  "max_drift_m": 10.76168896624531,
  "radial_IAE_m_s": 321.53067898333586,
  "signed_longitudinal_delta_m": -10.679549420757573,
  "tail_speed_mean_m_s": -0.18153267759681374,
  "tail_speed_rms_m_s": 0.18153277599719733,
  "tail_sensor_speed_mean_m_s": -0.1811441782637925,
  "tail_fk_speed_mean_m_s": -0.18113830802370848,
  "peak_tilt_rad": 0.029392044718075327,
  "peak_wheel_torque_nm": 0.28778690099716187,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 12.768352011975367
}
```
