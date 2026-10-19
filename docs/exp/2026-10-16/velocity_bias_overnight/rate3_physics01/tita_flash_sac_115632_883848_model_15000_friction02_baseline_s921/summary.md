# tita_flash_sac_115632_883848_model_15000_friction02_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 966f7a286b3139a7c633828fa375c6eeb4645d5eed73f64ed986c1c72dc72003

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_15000_friction02_baseline_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_15000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "friction": 0.2
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
  "initial_physics_sha256": "b13d023a20fcb3c8cc62e5636d60816ef37aa0811b18c38ce933ee40c75b28bd",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 6.458665718605118,
  "max_drift_m": 6.458665718605118,
  "radial_IAE_m_s": 199.59811253385848,
  "signed_longitudinal_delta_m": -6.348979924381102,
  "tail_speed_mean_m_s": -0.10157960351516121,
  "tail_speed_rms_m_s": 0.10159041111268206,
  "tail_sensor_speed_mean_m_s": -0.1014229229358809,
  "tail_fk_speed_mean_m_s": -0.10141796252548216,
  "peak_tilt_rad": 0.06375063106225687,
  "peak_wheel_torque_nm": 1.861644983291626,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 10.43567716900725
}
```
