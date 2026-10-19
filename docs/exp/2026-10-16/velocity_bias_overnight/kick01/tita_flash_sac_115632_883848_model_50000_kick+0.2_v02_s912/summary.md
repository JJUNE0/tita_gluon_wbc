# tita_flash_sac_115632_883848_model_50000_kick+0.2_v02_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d5b7c981c4c4cd5375fd5513ec12f02c7abada4ca21df8727729faf1d0e31e7c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_50000_kick+0.2_v02_s912",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_50000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 912,
    "estimator": "fk",
    "runtime": true,
    "kick": 0.2,
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
  "initial_physics_sha256": "4ac873f1fbca167075e398d1e93efe0c26d927d37ca08e6783d7c255bd917c81",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.0028418666425798988,
  "max_drift_m": 0.07389423901616832,
  "radial_IAE_m_s": 0.24772102545857622,
  "signed_longitudinal_delta_m": 0.002835747333416738,
  "tail_speed_mean_m_s": -6.117326515604054e-07,
  "tail_speed_rms_m_s": 2.0432002522741666e-06,
  "tail_sensor_speed_mean_m_s": -4.1932183420843136e-07,
  "tail_fk_speed_mean_m_s": 1.993673720708319e-06,
  "peak_tilt_rad": 0.0780610608330321,
  "peak_wheel_torque_nm": 1.7495357990264893,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.021812408373039115,
  "final_integral_m_s": 0.021814211821436703,
  "elapsed_wall_s": 14.568309618043713
}
```
