# tita_flash_sac_115632_883848_model_15000_kick-0.2_v04_s922

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 966f7a286b3139a7c633828fa375c6eeb4645d5eed73f64ed986c1c72dc72003

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_15000_kick-0.2_v04_s922",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_15000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 922,
    "estimator": "fk",
    "guarded": true,
    "kick": -0.2,
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
  "initial_physics_sha256": "07de3a562d087f08d54035ad69350af113d1207591b8cfb06655b9b8f9e2a3c9",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.03152862002667708,
  "max_drift_m": 0.08671883252258165,
  "radial_IAE_m_s": 1.9928312529154728,
  "signed_longitudinal_delta_m": -0.031474213122600916,
  "tail_speed_mean_m_s": 2.50054922791734e-05,
  "tail_speed_rms_m_s": 2.7096480270702598e-05,
  "tail_sensor_speed_mean_m_s": 2.52301900258875e-05,
  "tail_fk_speed_mean_m_s": 2.583926568955423e-05,
  "peak_tilt_rad": 0.14261853125766177,
  "peak_wheel_torque_nm": 4.129051208496094,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.36681608990672615,
  "final_integral_m_s": -0.36681608990672615,
  "elapsed_wall_s": 9.06069137895247
}
```
