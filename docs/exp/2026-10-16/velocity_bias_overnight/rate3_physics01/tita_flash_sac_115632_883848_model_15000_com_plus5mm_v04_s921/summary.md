# tita_flash_sac_115632_883848_model_15000_com_plus5mm_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 966f7a286b3139a7c633828fa375c6eeb4645d5eed73f64ed986c1c72dc72003

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_15000_com_plus5mm_v04_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_15000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "com": 0.005
    },
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
  "initial_physics_sha256": "3c7d8199727bbeae85b41226d2a74e2b9de425416d84d5385359b99558bf4662",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.03481489341193747,
  "max_drift_m": 0.05033966922850504,
  "radial_IAE_m_s": 2.1431923119269825,
  "signed_longitudinal_delta_m": -0.0347720025097202,
  "tail_speed_mean_m_s": 1.9540100072798165e-05,
  "tail_speed_rms_m_s": 1.9776658574157843e-05,
  "tail_sensor_speed_mean_m_s": 1.980486988996346e-05,
  "tail_fk_speed_mean_m_s": 2.048367670604911e-05,
  "peak_tilt_rad": 0.11824850116978225,
  "peak_wheel_torque_nm": 2.593000650405884,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.3295922905109629,
  "final_integral_m_s": -0.3295922905109629,
  "elapsed_wall_s": 10.52274111600127
}
```
