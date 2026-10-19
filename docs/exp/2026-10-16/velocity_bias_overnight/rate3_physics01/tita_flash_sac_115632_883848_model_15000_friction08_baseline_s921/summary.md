# tita_flash_sac_115632_883848_model_15000_friction08_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 966f7a286b3139a7c633828fa375c6eeb4645d5eed73f64ed986c1c72dc72003

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_15000_friction08_baseline_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_15000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "friction": 0.8
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
  "initial_physics_sha256": "9527102db3c57d10272c421c690ec360d1bff28f0c8bc6ef503d735a85f2a403",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 7.869734878867488,
  "max_drift_m": 7.869734878867488,
  "radial_IAE_m_s": 234.71948358736648,
  "signed_longitudinal_delta_m": -7.86074973001554,
  "tail_speed_mean_m_s": -0.13204683753697766,
  "tail_speed_rms_m_s": 0.13206625405496816,
  "tail_sensor_speed_mean_m_s": -0.13174136024245775,
  "tail_fk_speed_mean_m_s": -0.13179607282347128,
  "peak_tilt_rad": 0.05882263429801404,
  "peak_wheel_torque_nm": 2.024669647216797,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 10.031595130974893
}
```
