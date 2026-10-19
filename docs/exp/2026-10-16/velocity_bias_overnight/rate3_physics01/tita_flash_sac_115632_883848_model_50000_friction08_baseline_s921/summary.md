# tita_flash_sac_115632_883848_model_50000_friction08_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d5b7c981c4c4cd5375fd5513ec12f02c7abada4ca21df8727729faf1d0e31e7c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_50000_friction08_baseline_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_50000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "friction": 0.8
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
  "initial_physics_sha256": "caf13f8d52a59454ba9731f604b2348293f6c7d4f198d188537972569670558b",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.5167363786017405,
  "max_drift_m": 0.5167363786017405,
  "radial_IAE_m_s": 14.782731524754926,
  "signed_longitudinal_delta_m": 0.43522717668448524,
  "tail_speed_mean_m_s": 0.00938879578520973,
  "tail_speed_rms_m_s": 0.009388927344586347,
  "tail_sensor_speed_mean_m_s": 0.009370723280007407,
  "tail_fk_speed_mean_m_s": 0.009372764626826348,
  "peak_tilt_rad": 0.041595965057339646,
  "peak_wheel_torque_nm": 0.29918771982192993,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 8.283871926018037
}
```
