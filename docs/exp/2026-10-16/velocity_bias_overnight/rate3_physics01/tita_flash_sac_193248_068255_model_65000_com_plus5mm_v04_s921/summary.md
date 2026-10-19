# tita_flash_sac_193248_068255_model_65000_com_plus5mm_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 950b5958dfae8344a2f3cfbf5d26f83d6cac60eaaf404962bb8ea0b163f7244e

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_65000_com_plus5mm_v04_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_65000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "com": 0.005
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
  "initial_physics_sha256": "72da7550c4b0f1931d3de2b0b155ebe7ffd9411bec2ca24f87d880dc26ad3c28",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.0020667974842431694,
  "max_drift_m": 0.010093783140952455,
  "radial_IAE_m_s": 0.23969115985959386,
  "signed_longitudinal_delta_m": -0.0020479379732047803,
  "tail_speed_mean_m_s": 5.687321088524603e-05,
  "tail_speed_rms_m_s": 5.687912684319118e-05,
  "tail_sensor_speed_mean_m_s": 5.6320151912313115e-05,
  "tail_fk_speed_mean_m_s": 5.791089001912425e-05,
  "peak_tilt_rad": 0.038147455174187384,
  "peak_wheel_torque_nm": 0.11402271687984467,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.04527817437374552,
  "final_integral_m_s": -0.04527817437374552,
  "elapsed_wall_s": 8.276189608033746
}
```
