# tita_flash_sac_115632_883848_model_50000_friction02_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d5b7c981c4c4cd5375fd5513ec12f02c7abada4ca21df8727729faf1d0e31e7c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_50000_friction02_baseline_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_50000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "friction": 0.2
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
  "initial_physics_sha256": "f5f168ea9590afd458db6be3c8fb9e89977091d89c192c3ab60cfdaafd25fa0f",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.12244411194846715,
  "max_drift_m": 0.328090431682473,
  "radial_IAE_m_s": 13.732011335374589,
  "signed_longitudinal_delta_m": -0.031829582439417504,
  "tail_speed_mean_m_s": 0.010179148346047646,
  "tail_speed_rms_m_s": 0.010191978306611038,
  "tail_sensor_speed_mean_m_s": 0.010293669795324794,
  "tail_fk_speed_mean_m_s": 0.010194802568888387,
  "peak_tilt_rad": 0.04025033063427075,
  "peak_wheel_torque_nm": 0.14171969890594482,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.620036612963304
}
```
