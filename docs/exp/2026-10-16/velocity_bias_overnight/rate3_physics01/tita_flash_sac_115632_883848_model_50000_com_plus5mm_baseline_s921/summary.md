# tita_flash_sac_115632_883848_model_50000_com_plus5mm_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d5b7c981c4c4cd5375fd5513ec12f02c7abada4ca21df8727729faf1d0e31e7c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_50000_com_plus5mm_baseline_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_50000",
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
  "initial_physics_sha256": "5f97c4d06ece6a57496e3ab1870245beddbfc8a15ba8a24b45ac04f19d1c53bd",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 1.7863289755167249,
  "max_drift_m": 1.7863289755167249,
  "radial_IAE_m_s": 54.09775529054529,
  "signed_longitudinal_delta_m": 1.7456635101314686,
  "tail_speed_mean_m_s": 0.029414569718986018,
  "tail_speed_rms_m_s": 0.02941500619805746,
  "tail_sensor_speed_mean_m_s": 0.029351189888341653,
  "tail_fk_speed_mean_m_s": 0.02935321325495841,
  "peak_tilt_rad": 0.048997869746188805,
  "peak_wheel_torque_nm": 0.315529465675354,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 7.0252853040001355
}
```
