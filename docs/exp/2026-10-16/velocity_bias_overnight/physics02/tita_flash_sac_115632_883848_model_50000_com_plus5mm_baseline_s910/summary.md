# tita_flash_sac_115632_883848_model_50000_com_plus5mm_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d5b7c981c4c4cd5375fd5513ec12f02c7abada4ca21df8727729faf1d0e31e7c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_50000_com_plus5mm_baseline_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_50000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "com": 0.005
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "d5b7c981c4c4cd5375fd5513ec12f02c7abada4ca21df8727729faf1d0e31e7c",
  "onnx_sha256": "0128f5783513e86a2d0cfbc67ed5d02260d017356909fa01ccf0635c03248873",
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
  "initial_physics_sha256": "fb2dcd6eb7e7d8ccdd291dab60fe2d2de9f332181e2d94a6343b48fab011d954",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 1.7825285877432222,
  "max_drift_m": 1.7825285877432222,
  "radial_IAE_m_s": 53.803732102108334,
  "signed_longitudinal_delta_m": 1.7084195490871998,
  "tail_speed_mean_m_s": 0.029510006274462673,
  "tail_speed_rms_m_s": 0.02951038518005726,
  "tail_sensor_speed_mean_m_s": 0.029447051062746515,
  "tail_fk_speed_mean_m_s": 0.029449029172671694,
  "peak_tilt_rad": 0.04892425919580434,
  "peak_wheel_torque_nm": 0.31552988290786743,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.57791787100723
}
```
