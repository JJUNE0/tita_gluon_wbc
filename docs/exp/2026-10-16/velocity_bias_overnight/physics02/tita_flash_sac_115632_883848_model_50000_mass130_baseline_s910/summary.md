# tita_flash_sac_115632_883848_model_50000_mass130_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d5b7c981c4c4cd5375fd5513ec12f02c7abada4ca21df8727729faf1d0e31e7c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_50000_mass130_baseline_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_50000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "mass": 1.3
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
  "initial_physics_sha256": "1a59aa57175bcc0057e4806670f746d323d4943c085900be324d4a7e172aa551",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 8.50900633834556,
  "max_drift_m": 8.50900633834556,
  "radial_IAE_m_s": 255.6040641195227,
  "signed_longitudinal_delta_m": -8.37931314933246,
  "tail_speed_mean_m_s": -0.14281745657957964,
  "tail_speed_rms_m_s": 0.14281746276589008,
  "tail_sensor_speed_mean_m_s": -0.14252720682824602,
  "tail_fk_speed_mean_m_s": -0.1425180600471361,
  "peak_tilt_rad": 0.04124944981094725,
  "peak_wheel_torque_nm": 0.29736536741256714,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.59433121199254
}
```
