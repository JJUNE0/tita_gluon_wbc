# tita_flash_sac_193248_068255_model_20000_kick+0.2_baseline_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 4bb0e92e03390c3256497280f4ab3eda89d64ce8dfc23bfd9d799d69aa0d068c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_20000_kick+0.2_baseline_s917",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_20000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 917,
    "estimator": "fk",
    "guarded": false,
    "kick": 0.2,
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
  },
  "checkpoint_sha256": "4bb0e92e03390c3256497280f4ab3eda89d64ce8dfc23bfd9d799d69aa0d068c",
  "onnx_sha256": "a24d51f2c61ac25fc44c8e657cd90494575b17855d820a382e66b027caddbaac",
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
  "initial_physics_sha256": "8fafdbc55603c6e52bee0c99e0346e19fea0f5e9af13304d3d2e09a5f2449fc4",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 13.124967524060033,
  "max_drift_m": 13.124967524060033,
  "radial_IAE_m_s": 396.53266336322406,
  "signed_longitudinal_delta_m": 13.091114676984251,
  "tail_speed_mean_m_s": 0.21848311869099088,
  "tail_speed_rms_m_s": 0.2184831187270918,
  "tail_sensor_speed_mean_m_s": 0.2180116293155978,
  "tail_fk_speed_mean_m_s": 0.21800171554923634,
  "peak_tilt_rad": 0.17848968970170986,
  "peak_wheel_torque_nm": 2.7637627124786377,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 8.558491944975685
}
```
