# tita_flash_sac_115632_883848_model_15000_mass130_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 966f7a286b3139a7c633828fa375c6eeb4645d5eed73f64ed986c1c72dc72003

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_15000_mass130_baseline_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_15000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "mass": 1.3
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
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
  "initial_physics_sha256": "4b0308026d7b54ab447e5b86c6ea0f327201694679c481414a65b30b963bbdef",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 3.9659619201228775,
  "max_drift_m": 3.9659619201228775,
  "radial_IAE_m_s": 119.57616804401007,
  "signed_longitudinal_delta_m": -3.941257549576721,
  "tail_speed_mean_m_s": -0.06596915221481602,
  "tail_speed_rms_m_s": 0.0743758825616968,
  "tail_sensor_speed_mean_m_s": -0.06963272178794298,
  "tail_fk_speed_mean_m_s": -0.06656682223847839,
  "peak_tilt_rad": 0.15112060313349351,
  "peak_wheel_torque_nm": 6.851764678955078,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 11.487377329962328
}
```
