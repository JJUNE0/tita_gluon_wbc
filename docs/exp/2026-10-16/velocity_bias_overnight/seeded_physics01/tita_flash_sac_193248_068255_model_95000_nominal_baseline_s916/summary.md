# tita_flash_sac_193248_068255_model_95000_nominal_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a9ca81d693e2ee34f29bbb8746ae6c7a09f1a201d1d579d15a861fab83818441

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_95000_nominal_baseline_s916",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_95000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": false,
    "physics": {},
    "law": {
      "mode": "constant",
      "bias": 0.0
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
  "initial_physics_sha256": "2e4b78a84e35bc3698458065547b664ea03339fb521367a6642c0bb41f949b8d",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 8.512319127286196,
  "max_drift_m": 8.512319127286196,
  "radial_IAE_m_s": 230.83011996384198,
  "signed_longitudinal_delta_m": -8.308119525613426,
  "tail_speed_mean_m_s": -0.1760155477637226,
  "tail_speed_rms_m_s": 0.17698182692470138,
  "tail_sensor_speed_mean_m_s": -0.1757897745161595,
  "tail_fk_speed_mean_m_s": -0.17581127368481508,
  "peak_tilt_rad": 0.04488592586942408,
  "peak_wheel_torque_nm": 0.2235138714313507,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.773587425006554
}
```
