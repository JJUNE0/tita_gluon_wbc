# tita_flash_sac_193248_068255_model_95000_nominal_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a9ca81d693e2ee34f29bbb8746ae6c7a09f1a201d1d579d15a861fab83818441

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_95000_nominal_baseline_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_95000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": false,
    "physics": {},
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
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
  "initial_physics_sha256": "203d50b5df07ff49ae6b4d509582eb0ea13a80ee4156c7e2de5db58c90428736",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 8.512317882881547,
  "max_drift_m": 8.512317882881547,
  "radial_IAE_m_s": 230.8301081526587,
  "signed_longitudinal_delta_m": -8.308118589738358,
  "tail_speed_mean_m_s": -0.17601548705314543,
  "tail_speed_rms_m_s": 0.17698176470207533,
  "tail_sensor_speed_mean_m_s": -0.17578971349859301,
  "tail_fk_speed_mean_m_s": -0.1758112129830957,
  "peak_tilt_rad": 0.04488596175610904,
  "peak_wheel_torque_nm": 0.22351300716400146,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 6.236028034996707
}
```
