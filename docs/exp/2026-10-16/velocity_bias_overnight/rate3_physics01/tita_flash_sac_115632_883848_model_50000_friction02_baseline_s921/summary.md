# tita_flash_sac_115632_883848_model_50000_friction02_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d5b7c981c4c4cd5375fd5513ec12f02c7abada4ca21df8727729faf1d0e31e7c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_50000_friction02_baseline_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_50000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "friction": 0.2
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
  "initial_physics_sha256": "c0c057b81ac3e420b537219c586f35a118fd3e56d8da6ef440e210dd3864dc32",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.12244470652772489,
  "max_drift_m": 0.32808816352739983,
  "radial_IAE_m_s": 13.73189329043058,
  "signed_longitudinal_delta_m": -0.03182828792313857,
  "tail_speed_mean_m_s": 0.01017905168900351,
  "tail_speed_rms_m_s": 0.010191873507261851,
  "tail_sensor_speed_mean_m_s": 0.010293577666535948,
  "tail_fk_speed_mean_m_s": 0.01019470665794256,
  "peak_tilt_rad": 0.04024488678668825,
  "peak_wheel_torque_nm": 0.14162485301494598,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 6.296283297997434
}
```
