# tita_flash_sac_115632_883848_model_50000_mass115_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d5b7c981c4c4cd5375fd5513ec12f02c7abada4ca21df8727729faf1d0e31e7c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_50000_mass115_baseline_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_50000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "mass": 1.15
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
  "initial_physics_sha256": "240f9f2b852d4df0c217a64d60a7cef4116707a842502ed6e18f892ba61df5f8",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 5.2737897196868895,
  "max_drift_m": 5.2737897196868895,
  "radial_IAE_m_s": 155.2488155342282,
  "signed_longitudinal_delta_m": -5.212511048757502,
  "tail_speed_mean_m_s": -0.09120608296006416,
  "tail_speed_rms_m_s": 0.09120795020811885,
  "tail_sensor_speed_mean_m_s": -0.0910089638731255,
  "tail_fk_speed_mean_m_s": -0.09100551894753366,
  "peak_tilt_rad": 0.047515654728570667,
  "peak_wheel_torque_nm": 0.3089331090450287,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 8.959024961979594
}
```
