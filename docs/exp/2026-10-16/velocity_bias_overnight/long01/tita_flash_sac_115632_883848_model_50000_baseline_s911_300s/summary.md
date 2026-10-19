# tita_flash_sac_115632_883848_model_50000_baseline_s911_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d5b7c981c4c4cd5375fd5513ec12f02c7abada4ca21df8727729faf1d0e31e7c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_50000_baseline_s911_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_50000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 911,
    "estimator": "fk",
    "runtime": false,
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
  "initial_physics_sha256": "2e33055c924368ffff9686dcc9254019ff155ac89c6707b422254f90a170a961",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 3.003734244672373,
  "max_drift_m": 3.003734244672373,
  "radial_IAE_m_s": 428.20022687718506,
  "signed_longitudinal_delta_m": 2.2485388796172567,
  "tail_speed_mean_m_s": 0.013115586742636843,
  "tail_speed_rms_m_s": 0.013115602121656925,
  "tail_sensor_speed_mean_m_s": 0.013094749052509392,
  "tail_fk_speed_mean_m_s": 0.013096668478196627,
  "peak_tilt_rad": 0.04181293722127433,
  "peak_wheel_torque_nm": 0.29949048161506653,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 39.93209750298411
}
```
