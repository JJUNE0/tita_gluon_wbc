# tita_flash_sac_115632_883848_model_15000_nominal_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 966f7a286b3139a7c633828fa375c6eeb4645d5eed73f64ed986c1c72dc72003

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_15000_nominal_baseline_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_15000",
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
  "initial_physics_sha256": "1696bd2003b0303ab4db4f0d1a2484c0cdb28c82d28ac0e19fc1ff291d290d9a",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 7.637622792176352,
  "max_drift_m": 7.637622792176352,
  "radial_IAE_m_s": 230.3823771294915,
  "signed_longitudinal_delta_m": -7.596668472366935,
  "tail_speed_mean_m_s": -0.12579811098811516,
  "tail_speed_rms_m_s": 0.1258016404582133,
  "tail_sensor_speed_mean_m_s": -0.12556610202786797,
  "tail_fk_speed_mean_m_s": -0.1255487431091472,
  "peak_tilt_rad": 0.05868311445552776,
  "peak_wheel_torque_nm": 1.9245706796646118,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 8.708637745003216
}
```
