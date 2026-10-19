# tita_flash_sac_193248_068255_model_20000_nominal_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 4bb0e92e03390c3256497280f4ab3eda89d64ce8dfc23bfd9d799d69aa0d068c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_20000_nominal_baseline_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_20000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": false,
    "physics": {},
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
  "initial_physics_sha256": "980afb619459ab75c6dc361933b3923d25666c64cbc6d38c62c8fa0914381882",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 13.033275672299911,
  "max_drift_m": 13.033275672299911,
  "radial_IAE_m_s": 391.02260526070523,
  "signed_longitudinal_delta_m": 13.002280189445328,
  "tail_speed_mean_m_s": 0.21848274142160726,
  "tail_speed_rms_m_s": 0.21848274146277571,
  "tail_sensor_speed_mean_m_s": 0.21801128296150293,
  "tail_fk_speed_mean_m_s": 0.21800133858974963,
  "peak_tilt_rad": 0.1595556854614384,
  "peak_wheel_torque_nm": 0.40741825103759766,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 7.9903111279709265
}
```
