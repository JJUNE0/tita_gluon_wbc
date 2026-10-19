# tita_flash_sac_193248_068255_model_20000_kick-0.2_baseline_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 4bb0e92e03390c3256497280f4ab3eda89d64ce8dfc23bfd9d799d69aa0d068c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_20000_kick-0.2_baseline_s917",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_20000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 917,
    "estimator": "fk",
    "guarded": false,
    "kick": -0.2,
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
  "initial_physics_sha256": "d4f4c238d53132f68a8618137ca7fbf12f04b1f59757e005353eeffb3ed80d96",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 12.93107247045654,
  "max_drift_m": 12.93107247045654,
  "radial_IAE_m_s": 384.89274425784697,
  "signed_longitudinal_delta_m": 12.902756771735554,
  "tail_speed_mean_m_s": 0.21848230656336867,
  "tail_speed_rms_m_s": 0.21848230660941817,
  "tail_sensor_speed_mean_m_s": 0.21801086058682168,
  "tail_fk_speed_mean_m_s": 0.21800090547727258,
  "peak_tilt_rad": 0.1595551171701377,
  "peak_wheel_torque_nm": 1.5432559251785278,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 8.720556774002034
}
```
