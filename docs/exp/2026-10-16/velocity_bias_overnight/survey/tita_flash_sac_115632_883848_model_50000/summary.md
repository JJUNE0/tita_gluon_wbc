# tita_flash_sac_115632_883848_model_50000

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d5b7c981c4c4cd5375fd5513ec12f02c7abada4ca21df8727729faf1d0e31e7c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_50000",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_50000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 270,
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
  "initial_physics_sha256": "992f7d81a13cfab39b5161a7c113c3a5484d3f122f83d262ce52d922fa183f51",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.5455138743088432,
  "max_drift_m": 0.5455138743088432,
  "radial_IAE_m_s": 16.118161258280367,
  "signed_longitudinal_delta_m": 0.539484924502649,
  "tail_speed_mean_m_s": 0.009387296345324782,
  "tail_speed_rms_m_s": 0.00938734644159529,
  "tail_sensor_speed_mean_m_s": 0.009367283440139765,
  "tail_fk_speed_mean_m_s": 0.00936948180809854,
  "peak_tilt_rad": 0.039722633904514915,
  "peak_wheel_torque_nm": 0.29949021339416504,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 4.518173902994022
}
```
