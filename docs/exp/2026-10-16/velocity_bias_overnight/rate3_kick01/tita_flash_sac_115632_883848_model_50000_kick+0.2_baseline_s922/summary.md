# tita_flash_sac_115632_883848_model_50000_kick+0.2_baseline_s922

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d5b7c981c4c4cd5375fd5513ec12f02c7abada4ca21df8727729faf1d0e31e7c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_50000_kick+0.2_baseline_s922",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_50000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 922,
    "estimator": "fk",
    "guarded": false,
    "kick": 0.2,
    "law": {
      "mode": "constant",
      "bias": 0.0
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
  "final_drift_m": 0.6843901544948184,
  "max_drift_m": 0.6843901544948184,
  "radial_IAE_m_s": 24.572972461222367,
  "signed_longitudinal_delta_m": 0.6748466605431095,
  "tail_speed_mean_m_s": 0.009341873138394989,
  "tail_speed_rms_m_s": 0.009342003968355207,
  "tail_sensor_speed_mean_m_s": 0.009321929680459995,
  "tail_fk_speed_mean_m_s": 0.009324148514399944,
  "peak_tilt_rad": 0.08115023226965601,
  "peak_wheel_torque_nm": 1.5053824186325073,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 8.830114958051126
}
```
