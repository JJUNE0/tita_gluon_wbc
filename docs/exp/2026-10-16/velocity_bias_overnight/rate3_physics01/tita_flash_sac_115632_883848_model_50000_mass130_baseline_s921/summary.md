# tita_flash_sac_115632_883848_model_50000_mass130_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d5b7c981c4c4cd5375fd5513ec12f02c7abada4ca21df8727729faf1d0e31e7c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_50000_mass130_baseline_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_50000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "mass": 1.3
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
  },
  "checkpoint_sha256": "d5b7c981c4c4cd5375fd5513ec12f02c7abada4ca21df8727729faf1d0e31e7c",
  "onnx_sha256": "0128f5783513e86a2d0cfbc67ed5d02260d017356909fa01ccf0635c03248873",
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
  "initial_physics_sha256": "5dcb00be120861b4be8cd87d0d904f02bfb42b46bc5be94babcf5da1af422652",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 8.50900650295267,
  "max_drift_m": 8.50900650295267,
  "radial_IAE_m_s": 255.6040775729874,
  "signed_longitudinal_delta_m": -8.379313385760248,
  "tail_speed_mean_m_s": -0.14281745121454104,
  "tail_speed_rms_m_s": 0.14281745739234344,
  "tail_sensor_speed_mean_m_s": -0.14252720178653075,
  "tail_fk_speed_mean_m_s": -0.14251805455675015,
  "peak_tilt_rad": 0.04124944240159545,
  "peak_wheel_torque_nm": 0.29735302925109863,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 7.302737928985152
}
```
