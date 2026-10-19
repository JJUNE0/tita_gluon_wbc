# tita_flash_sac_115632_883848_model_95000_kick+0.2_v03_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 7fc976ceb0b69090d3baf26399d36e566e21da7bf1a3f935bf0a1bc7b29a5d82

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_95000_kick+0.2_v03_s917",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_95000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 917,
    "estimator": "fk",
    "guarded": true,
    "kick": 0.2,
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
  "checkpoint_sha256": "7fc976ceb0b69090d3baf26399d36e566e21da7bf1a3f935bf0a1bc7b29a5d82",
  "onnx_sha256": "1a45e6567675d4dfc1a738bbe430e52a4f2a2cab73c2c908c46928d22bd54530",
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
  "initial_physics_sha256": "ac86d505f4a747b4252fb406a75f1739e6c266243d13bf0b115e3d9332e179b4",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.033733999049544834,
  "max_drift_m": 0.12489386253326314,
  "radial_IAE_m_s": 1.8122413126757135,
  "signed_longitudinal_delta_m": 0.03373399830675807,
  "tail_speed_mean_m_s": 0.00024082086521082878,
  "tail_speed_rms_m_s": 0.00024374603811014352,
  "tail_sensor_speed_mean_m_s": 0.00024022425339818412,
  "tail_fk_speed_mean_m_s": 0.00024081828798534248,
  "peak_tilt_rad": 0.0822735515718831,
  "peak_wheel_torque_nm": 1.8285995721817017,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.08159493092912595,
  "final_integral_m_s": 0.08159493092912595,
  "elapsed_wall_s": 10.545057591982186
}
```
