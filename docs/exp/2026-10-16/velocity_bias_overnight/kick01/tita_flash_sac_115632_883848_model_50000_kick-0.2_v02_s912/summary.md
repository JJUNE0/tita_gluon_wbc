# tita_flash_sac_115632_883848_model_50000_kick-0.2_v02_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d5b7c981c4c4cd5375fd5513ec12f02c7abada4ca21df8727729faf1d0e31e7c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_50000_kick-0.2_v02_s912",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_50000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 912,
    "estimator": "fk",
    "runtime": true,
    "kick": -0.2,
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
  "initial_physics_sha256": "b81b48855dbf88a2c33cd0b9168e617e88bbcbda6e0e767eb738833acec79e3b",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.002011003408088793,
  "max_drift_m": 0.06217248369380894,
  "radial_IAE_m_s": 0.1655596344466485,
  "signed_longitudinal_delta_m": 6.31616497950119e-05,
  "tail_speed_mean_m_s": -4.0935339229265313e-07,
  "tail_speed_rms_m_s": 2.0054305501548965e-06,
  "tail_sensor_speed_mean_m_s": -2.2134295916717461e-07,
  "tail_fk_speed_mean_m_s": 2.1929484215922573e-06,
  "peak_tilt_rad": 0.11161492837009845,
  "peak_wheel_torque_nm": 1.4577142000198364,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.021818912005516358,
  "final_integral_m_s": 0.021818774019966725,
  "elapsed_wall_s": 17.463590611994732
}
```
