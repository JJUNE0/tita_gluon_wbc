# tita_flash_sac_115632_883848_model_10000_friction08_v03_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 48a0379d0b30385cff5ccfe473d0ee136f303e640a505719a82bad5a3e3178a5

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_10000_friction08_v03_s916",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_10000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "friction": 0.8
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
  "checkpoint_sha256": "48a0379d0b30385cff5ccfe473d0ee136f303e640a505719a82bad5a3e3178a5",
  "onnx_sha256": "06e48800bb84c9f9275464d939d3614105bfbc1bbe6af1e92522c94faa5f1e15",
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
  "initial_physics_sha256": "2fffea5bf2319e22e9506584929a42900f25e890b39121d154ab27c2a5e34fd9",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.09189480190275277,
  "max_drift_m": 0.11351977987930774,
  "radial_IAE_m_s": 5.960346284625169,
  "signed_longitudinal_delta_m": 0.09189407921520346,
  "tail_speed_mean_m_s": -0.0007528456718126009,
  "tail_speed_rms_m_s": 0.017603385224884135,
  "tail_sensor_speed_mean_m_s": -0.000808679864909609,
  "tail_fk_speed_mean_m_s": -0.0009172572588645912,
  "peak_tilt_rad": 0.11404978193451965,
  "peak_wheel_torque_nm": 2.7237138748168945,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.3918846233666829,
  "final_integral_m_s": 0.3918846233666829,
  "elapsed_wall_s": 10.343665418971796
}
```
