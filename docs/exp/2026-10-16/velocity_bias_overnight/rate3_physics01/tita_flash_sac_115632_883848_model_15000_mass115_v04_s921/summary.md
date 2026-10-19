# tita_flash_sac_115632_883848_model_15000_mass115_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 966f7a286b3139a7c633828fa375c6eeb4645d5eed73f64ed986c1c72dc72003

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_15000_mass115_v04_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_15000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "mass": 1.15
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
  "initial_physics_sha256": "aee75ba61bcebbcf8b2be5d5d24f0667c1a538ef617ad07aa77c65423e4addf6",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.06558874549891781,
  "max_drift_m": 0.07669249393151328,
  "radial_IAE_m_s": 4.144026997616121,
  "signed_longitudinal_delta_m": -0.06551994814233592,
  "tail_speed_mean_m_s": 9.360401122980656e-05,
  "tail_speed_rms_m_s": 0.011956195712780587,
  "tail_sensor_speed_mean_m_s": 0.0010781561211611983,
  "tail_fk_speed_mean_m_s": 4.8906083065523876e-05,
  "peak_tilt_rad": 0.14793704120216788,
  "peak_wheel_torque_nm": 5.5997819900512695,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.4048731884949893,
  "final_integral_m_s": -0.4048731884949893,
  "elapsed_wall_s": 10.321706365037244
}
```
