# tita_flash_sac_115632_883848_model_15000_com_minus5mm_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 966f7a286b3139a7c633828fa375c6eeb4645d5eed73f64ed986c1c72dc72003

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_15000_com_minus5mm_v02_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_15000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "com": -0.005
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
  "initial_physics_sha256": "16866ed5ba61977377968b6f192d069d4c4b5c05fb212a88d39648f716b5b725",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.038562305720207884,
  "max_drift_m": 0.04966504227711365,
  "radial_IAE_m_s": 2.3350255334841084,
  "signed_longitudinal_delta_m": -0.038516926545555684,
  "tail_speed_mean_m_s": 1.2719951856943391e-05,
  "tail_speed_rms_m_s": 1.2723318578531904e-05,
  "tail_sensor_speed_mean_m_s": 1.293803032607707e-05,
  "tail_fk_speed_mean_m_s": 1.3536377236645535e-05,
  "peak_tilt_rad": 0.12947279652511723,
  "peak_wheel_torque_nm": 2.3469018936157227,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.4093783390114678,
  "final_integral_m_s": -0.40940547099520336,
  "elapsed_wall_s": 17.41442616301356
}
```
