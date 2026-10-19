# tita_flash_sac_115632_883848_model_50000_kick-0.2_baseline_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d5b7c981c4c4cd5375fd5513ec12f02c7abada4ca21df8727729faf1d0e31e7c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_50000_kick-0.2_baseline_s912",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_50000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 912,
    "estimator": "fk",
    "runtime": false,
    "kick": -0.2,
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
  "initial_physics_sha256": "b81b48855dbf88a2c33cd0b9168e617e88bbcbda6e0e767eb738833acec79e3b",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.3995468801809296,
  "max_drift_m": 0.3995468801809296,
  "radial_IAE_m_s": 9.760415918697433,
  "signed_longitudinal_delta_m": 0.38312269111849495,
  "tail_speed_mean_m_s": 0.009334895642100525,
  "tail_speed_rms_m_s": 0.009335056726029743,
  "tail_sensor_speed_mean_m_s": 0.009314943858236105,
  "tail_fk_speed_mean_m_s": 0.009317181625127135,
  "peak_tilt_rad": 0.04181295588948619,
  "peak_wheel_torque_nm": 1.3779895305633545,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 8.949081400991417
}
```
