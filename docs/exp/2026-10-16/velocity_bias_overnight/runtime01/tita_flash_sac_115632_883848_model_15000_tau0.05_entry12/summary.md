# tita_flash_sac_115632_883848_model_15000_tau0.05_entry12

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 966f7a286b3139a7c633828fa375c6eeb4645d5eed73f64ed986c1c72dc72003

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_15000_tau0.05_entry12",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_15000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 271,
    "estimator": "fk",
    "runtime": true,
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.05,
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
  "initial_physics_sha256": "90341d8253a1eb02abdc274fcacb3ebd28667a54bafbf68c6c81061b3538307b",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.03479722610205212,
  "max_drift_m": 0.04171848199853395,
  "radial_IAE_m_s": 2.109333439315379,
  "signed_longitudinal_delta_m": -0.03475122255590469,
  "tail_speed_mean_m_s": 1.2121334238795229e-05,
  "tail_speed_rms_m_s": 1.290810842536542e-05,
  "tail_sensor_speed_mean_m_s": 1.2347182571146317e-05,
  "tail_fk_speed_mean_m_s": 1.2994463832870076e-05,
  "peak_tilt_rad": 0.12384102753980164,
  "peak_wheel_torque_nm": 2.6950221061706543,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.36722197027349013,
  "final_integral_m_s": -0.36723704063378243,
  "elapsed_wall_s": 5.856855637044646
}
```
