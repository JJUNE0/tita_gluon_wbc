# tita_flash_sac_115632_883848_model_15000_kick+0.2_v03_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 966f7a286b3139a7c633828fa375c6eeb4645d5eed73f64ed986c1c72dc72003

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_15000_kick+0.2_v03_s917",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_15000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 917,
    "estimator": "fk",
    "guarded": true,
    "kick": 0.2,
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
  "initial_physics_sha256": "42693931a3983bc267535b6a5fc3a8815a897a93f7916b47327296383079ce9a",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.028718757133628443,
  "max_drift_m": 0.03977405062192966,
  "radial_IAE_m_s": 1.7774622601344632,
  "signed_longitudinal_delta_m": -0.02866082382909736,
  "tail_speed_mean_m_s": 4.152689871366998e-05,
  "tail_speed_rms_m_s": 4.153699603820471e-05,
  "tail_sensor_speed_mean_m_s": 4.1654151403287285e-05,
  "tail_fk_speed_mean_m_s": 4.2341697105661275e-05,
  "peak_tilt_rad": 0.115999132024726,
  "peak_wheel_torque_nm": 3.035381317138672,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.36821627325543804,
  "final_integral_m_s": -0.36821627325543804,
  "elapsed_wall_s": 10.99996392702451
}
```
