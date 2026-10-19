# tita_flash_sac_115632_883848_model_15000_friction02_v03_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 966f7a286b3139a7c633828fa375c6eeb4645d5eed73f64ed986c1c72dc72003

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_15000_friction02_v03_s916",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_15000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "friction": 0.2
    },
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
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
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
  "initial_physics_sha256": "71c9f8a3835f51827813f13be241c761dad54de5762d52b5f850fcac8fc5c9ea",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.020728178815596573,
  "max_drift_m": 0.04028203421656184,
  "radial_IAE_m_s": 1.2716606879988688,
  "signed_longitudinal_delta_m": -0.02064554437377091,
  "tail_speed_mean_m_s": 7.846899737207424e-06,
  "tail_speed_rms_m_s": 7.851430589191308e-06,
  "tail_sensor_speed_mean_m_s": 7.999528441566341e-06,
  "tail_fk_speed_mean_m_s": 8.225444068861417e-06,
  "peak_tilt_rad": 0.12230600589941831,
  "peak_wheel_torque_nm": 2.618440628051758,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.3547971210684094,
  "final_integral_m_s": -0.3547971210684094,
  "elapsed_wall_s": 10.363254445022903
}
```
