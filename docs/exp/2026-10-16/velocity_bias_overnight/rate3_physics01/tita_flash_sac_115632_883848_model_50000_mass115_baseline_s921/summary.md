# tita_flash_sac_115632_883848_model_50000_mass115_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d5b7c981c4c4cd5375fd5513ec12f02c7abada4ca21df8727729faf1d0e31e7c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_50000_mass115_baseline_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_50000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "mass": 1.15
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
  "initial_physics_sha256": "0bebe853f44646fa3a2f455b9c2320f3e41f73c6ba7e96350c466944ecff585a",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 5.211599544365811,
  "max_drift_m": 5.211599544365811,
  "radial_IAE_m_s": 153.30679738844412,
  "signed_longitudinal_delta_m": -5.139695144673877,
  "tail_speed_mean_m_s": -0.09034189443183215,
  "tail_speed_rms_m_s": 0.09034420545671276,
  "tail_sensor_speed_mean_m_s": -0.0901466289487465,
  "tail_fk_speed_mean_m_s": -0.09014325128689206,
  "peak_tilt_rad": 0.04811207110552096,
  "peak_wheel_torque_nm": 0.3058229982852936,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 8.007918792020064
}
```
