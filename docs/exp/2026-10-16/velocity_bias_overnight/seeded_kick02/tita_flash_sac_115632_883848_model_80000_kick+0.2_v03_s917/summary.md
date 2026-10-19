# tita_flash_sac_115632_883848_model_80000_kick+0.2_v03_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 80677a4fd403aad22ca310d644998b9b9a686da481d6d95eaf8cc02aa67afadc

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_80000_kick+0.2_v03_s917",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_80000",
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
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
  },
  "checkpoint_sha256": "80677a4fd403aad22ca310d644998b9b9a686da481d6d95eaf8cc02aa67afadc",
  "onnx_sha256": "c7a83d6c9814cc6aa8357e4b0215d65d880dd6b756de2de920967396e901c93b",
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
  "initial_physics_sha256": "ff0ea9eb54537af6d3301b705c78d05253b17588ebdf67aa9d564c099f6087a3",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.13183080389166923,
  "max_drift_m": 0.209329871999747,
  "radial_IAE_m_s": 7.671938309048325,
  "signed_longitudinal_delta_m": 0.13180906429366424,
  "tail_speed_mean_m_s": 0.00012804499813950132,
  "tail_speed_rms_m_s": 0.00013391715785966243,
  "tail_sensor_speed_mean_m_s": 0.00012766179139540217,
  "tail_fk_speed_mean_m_s": 0.0001279514908163302,
  "peak_tilt_rad": 0.1022919032971179,
  "peak_wheel_torque_nm": 2.0844650268554688,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.8197061502531399,
  "final_integral_m_s": 0.8197061502531399,
  "elapsed_wall_s": 9.31992341199657
}
```
