# tita_flash_sac_115632_883848_model_15000_kick-0.2_v03_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 966f7a286b3139a7c633828fa375c6eeb4645d5eed73f64ed986c1c72dc72003

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_15000_kick-0.2_v03_s917",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_15000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 917,
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
  "initial_physics_sha256": "391a9b00e87e65f65a4b372bdebe9ea2cc73a9c5ae6502d07200b094889909f8",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.031627001849564726,
  "max_drift_m": 0.08809121733186642,
  "radial_IAE_m_s": 2.013765923409053,
  "signed_longitudinal_delta_m": -0.03157160232796875,
  "tail_speed_mean_m_s": 3.8077935911119635e-05,
  "tail_speed_rms_m_s": 3.901771681028587e-05,
  "tail_sensor_speed_mean_m_s": 3.822415951746065e-05,
  "tail_fk_speed_mean_m_s": 3.889885230740053e-05,
  "peak_tilt_rad": 0.14290492328628845,
  "peak_wheel_torque_nm": 4.183694362640381,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.3676439935596071,
  "final_integral_m_s": -0.3676439935596071,
  "elapsed_wall_s": 12.623964753001928
}
```
