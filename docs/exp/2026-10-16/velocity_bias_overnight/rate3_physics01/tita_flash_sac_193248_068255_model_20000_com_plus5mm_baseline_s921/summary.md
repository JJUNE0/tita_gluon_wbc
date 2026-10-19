# tita_flash_sac_193248_068255_model_20000_com_plus5mm_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 4bb0e92e03390c3256497280f4ab3eda89d64ce8dfc23bfd9d799d69aa0d068c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_20000_com_plus5mm_baseline_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_20000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "com": 0.005
    },
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
  "initial_physics_sha256": "bf2aabba8bdc224eece19ce5cdc2f152a263f93115feed45bed160f304bcb00e",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 13.949386013767848,
  "max_drift_m": 13.949386013767848,
  "radial_IAE_m_s": 418.4190033560899,
  "signed_longitudinal_delta_m": 13.915330909053248,
  "tail_speed_mean_m_s": 0.2337741520951272,
  "tail_speed_rms_m_s": 0.2337741521036533,
  "tail_sensor_speed_mean_m_s": 0.2332696625956821,
  "tail_fk_speed_mean_m_s": 0.23326131543083783,
  "peak_tilt_rad": 0.16602881118549928,
  "peak_wheel_torque_nm": 0.32204103469848633,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.14647892699577
}
```
