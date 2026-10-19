# p007_tita_flash_sac_115632_883848_model_15000

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 966f7a286b3139a7c633828fa375c6eeb4645d5eed73f64ed986c1c72dc72003

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "p007_tita_flash_sac_115632_883848_model_15000",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_15000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "physics": {
      "mass": 1.3
    },
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0,
      "gain_velocity": 0.1,
      "gain_tau": 0.3,
      "gain_floor": 0.25
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
  "initial_physics_sha256": "8a46eb8da72f4d8dcedc72e2f3114c61fb96b8817010954a82b7f026409f30c9",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.03906132005901269,
  "max_drift_m": 0.06785029646150202,
  "radial_IAE_m_s": 3.0792780056394733,
  "signed_longitudinal_delta_m": -0.03847816287258488,
  "tail_speed_mean_m_s": 0.0003872800065630859,
  "tail_speed_rms_m_s": 0.029170586289914445,
  "tail_sensor_speed_mean_m_s": -0.0011751155804067596,
  "tail_fk_speed_mean_m_s": -1.2482644494626826e-05,
  "peak_tilt_rad": 0.17950514479613067,
  "peak_wheel_torque_nm": 7.163858413696289,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.27595185541772105,
  "final_integral_m_s": -0.28290955871451995,
  "elapsed_wall_s": 14.165707165957429
}
```
