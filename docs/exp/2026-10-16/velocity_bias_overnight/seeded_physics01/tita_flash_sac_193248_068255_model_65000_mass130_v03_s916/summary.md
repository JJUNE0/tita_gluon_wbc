# tita_flash_sac_193248_068255_model_65000_mass130_v03_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 950b5958dfae8344a2f3cfbf5d26f83d6cac60eaaf404962bb8ea0b163f7244e

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_65000_mass130_v03_s916",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_65000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "mass": 1.3
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
  "checkpoint_sha256": "950b5958dfae8344a2f3cfbf5d26f83d6cac60eaaf404962bb8ea0b163f7244e",
  "onnx_sha256": "a1f326d5979e91ea8e5b962f09eb3e8da4d889ac9902563756ff9179048872c8",
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
  "initial_physics_sha256": "f67a190e92f81d6ff349a8d32e33ae1b988e9a536673d77c416ed89de7ea27cb",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.004782932341015045,
  "max_drift_m": 0.08882172612401648,
  "radial_IAE_m_s": 0.44803887469643705,
  "signed_longitudinal_delta_m": -0.004753208561349436,
  "tail_speed_mean_m_s": -1.2190174140402338e-07,
  "tail_speed_rms_m_s": 1.6797996955046847e-07,
  "tail_sensor_speed_mean_m_s": -7.473449057586728e-08,
  "tail_fk_speed_mean_m_s": 7.595758502033807e-08,
  "peak_tilt_rad": 0.15919155388826578,
  "peak_wheel_torque_nm": 0.9489849209785461,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.546113240927296,
  "final_integral_m_s": -0.546113240927296,
  "elapsed_wall_s": 12.566689621016849
}
```
