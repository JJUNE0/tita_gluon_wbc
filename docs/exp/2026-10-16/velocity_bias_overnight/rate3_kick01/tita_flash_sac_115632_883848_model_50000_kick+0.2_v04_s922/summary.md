# tita_flash_sac_115632_883848_model_50000_kick+0.2_v04_s922

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d5b7c981c4c4cd5375fd5513ec12f02c7abada4ca21df8727729faf1d0e31e7c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_50000_kick+0.2_v04_s922",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_50000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 922,
    "estimator": "fk",
    "guarded": true,
    "kick": 0.2,
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
  "initial_physics_sha256": "77fe435d14dd0b5149f4a62dde5b15d4b47cfd7774e2c638f51671b105a8baf4",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.0018295026978110338,
  "max_drift_m": 0.09382857308465584,
  "radial_IAE_m_s": 0.2808226784943574,
  "signed_longitudinal_delta_m": -0.0017200960605675362,
  "tail_speed_mean_m_s": 2.909960562316671e-06,
  "tail_speed_rms_m_s": 5.728225705406517e-06,
  "tail_sensor_speed_mean_m_s": 3.0952836958829167e-06,
  "tail_fk_speed_mean_m_s": 5.506412386957905e-06,
  "peak_tilt_rad": 0.0802878118365955,
  "peak_wheel_torque_nm": 1.5313931703567505,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.021380412979869153,
  "final_integral_m_s": 0.021380412979869153,
  "elapsed_wall_s": 9.529318192973733
}
```
