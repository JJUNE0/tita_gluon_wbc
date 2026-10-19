# tita_flash_sac_115632_883848_model_50000_mass115_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d5b7c981c4c4cd5375fd5513ec12f02c7abada4ca21df8727729faf1d0e31e7c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_50000_mass115_v02_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_50000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "mass": 1.15
    },
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
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
  "final_drift_m": 0.01378041564277673,
  "max_drift_m": 0.02812521179502873,
  "radial_IAE_m_s": 0.827519017672334,
  "signed_longitudinal_delta_m": -0.013745866509441379,
  "tail_speed_mean_m_s": -4.3230731958144624e-06,
  "tail_speed_rms_m_s": 4.718975143792969e-06,
  "tail_sensor_speed_mean_m_s": -3.7911345269598544e-06,
  "tail_fk_speed_mean_m_s": -2.261821213064668e-06,
  "peak_tilt_rad": 0.10028013245128053,
  "peak_wheel_torque_nm": 0.5957422852516174,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.142918902370098,
  "final_integral_m_s": -0.14292153703030178,
  "elapsed_wall_s": 12.30988715501735
}
```
