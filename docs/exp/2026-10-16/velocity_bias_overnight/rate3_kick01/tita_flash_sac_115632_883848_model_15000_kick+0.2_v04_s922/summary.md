# tita_flash_sac_115632_883848_model_15000_kick+0.2_v04_s922

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 966f7a286b3139a7c633828fa375c6eeb4645d5eed73f64ed986c1c72dc72003

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_15000_kick+0.2_v04_s922",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_15000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 922,
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
      "slew": 3.0,
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
  "initial_physics_sha256": "2a776fc0c1ad4e099a97361d59890cd279b56abc80e05243119bef8e3fa34da1",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.02857508058271904,
  "max_drift_m": 0.039750264430041156,
  "radial_IAE_m_s": 1.7575562243474716,
  "signed_longitudinal_delta_m": -0.0285175023123498,
  "tail_speed_mean_m_s": 3.1187793946240144e-05,
  "tail_speed_rms_m_s": 3.3199579634347395e-05,
  "tail_sensor_speed_mean_m_s": 3.138016844942511e-05,
  "tail_fk_speed_mean_m_s": 3.201577750631416e-05,
  "peak_tilt_rad": 0.11585341672075211,
  "peak_wheel_torque_nm": 3.0319104194641113,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.36720663974746703,
  "final_integral_m_s": -0.36720663974746703,
  "elapsed_wall_s": 8.886119702016003
}
```
