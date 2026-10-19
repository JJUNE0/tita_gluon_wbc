# tita_flash_sac_115632_883848_model_15000_friction08_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 966f7a286b3139a7c633828fa375c6eeb4645d5eed73f64ed986c1c72dc72003

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_15000_friction08_v02_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_15000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "friction": 0.8
    },
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
    }
  },
  "checkpoint_sha256": "966f7a286b3139a7c633828fa375c6eeb4645d5eed73f64ed986c1c72dc72003",
  "onnx_sha256": "1fec00b7bc7eebbc5b6decf23ac6f29b8799c5cf64ff1dee51c1ba762cf013ed",
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
  "initial_physics_sha256": "df2580fb2e7e89a20de9f3866b755d08b2d8321d5e309082c29fd17c387fc840",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.03525499451494128,
  "max_drift_m": 0.043968580580924226,
  "radial_IAE_m_s": 2.1461632970473223,
  "signed_longitudinal_delta_m": -0.035206119195604846,
  "tail_speed_mean_m_s": 1.6695263650919983e-05,
  "tail_speed_rms_m_s": 1.6768889226055754e-05,
  "tail_sensor_speed_mean_m_s": 1.6687236185013307e-05,
  "tail_fk_speed_mean_m_s": 1.7605981280576914e-05,
  "peak_tilt_rad": 0.12568959691889803,
  "peak_wheel_torque_nm": 2.71803617477417,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.3724250677569691,
  "final_integral_m_s": -0.37245876645590087,
  "elapsed_wall_s": 18.154783990001306
}
```
