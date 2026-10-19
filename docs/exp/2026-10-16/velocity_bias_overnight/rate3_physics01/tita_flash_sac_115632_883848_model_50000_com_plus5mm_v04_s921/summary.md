# tita_flash_sac_115632_883848_model_50000_com_plus5mm_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d5b7c981c4c4cd5375fd5513ec12f02c7abada4ca21df8727729faf1d0e31e7c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_50000_com_plus5mm_v04_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_50000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "com": 0.005
    },
    "law": {
      "kp": 0.0,
      "ki": 4.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 3.0,
      "seed_gain": 3.0
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
  "initial_physics_sha256": "5f97c4d06ece6a57496e3ab1870245beddbfc8a15ba8a24b45ac04f19d1c53bd",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.010823388222950092,
  "max_drift_m": 0.017854761003957654,
  "radial_IAE_m_s": 0.6478309550459556,
  "signed_longitudinal_delta_m": -0.01081956658000902,
  "tail_speed_mean_m_s": -2.7858368646547336e-06,
  "tail_speed_rms_m_s": 5.462815963079099e-06,
  "tail_sensor_speed_mean_m_s": -2.5719456467951756e-06,
  "tail_fk_speed_mean_m_s": -3.5872575660616335e-07,
  "peak_tilt_rad": 0.048997869746188805,
  "peak_wheel_torque_nm": 0.5208243727684021,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.060962393956516286,
  "final_integral_m_s": 0.060962393956516286,
  "elapsed_wall_s": 8.91343652701471
}
```
