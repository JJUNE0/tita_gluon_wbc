# tita_flash_sac_115632_883848_model_50000_nominal_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d5b7c981c4c4cd5375fd5513ec12f02c7abada4ca21df8727729faf1d0e31e7c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_50000_nominal_baseline_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_50000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {},
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
  "initial_physics_sha256": "ee3751db2ab4807246b1cc3aba6d175fbf7161aeccdc4924dc50e14f6493d7a2",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.539554777037189,
  "max_drift_m": 0.539554777037189,
  "radial_IAE_m_s": 15.908066010946417,
  "signed_longitudinal_delta_m": 0.5276939250920979,
  "tail_speed_mean_m_s": 0.00933950910912149,
  "tail_speed_rms_m_s": 0.009339641657079734,
  "tail_sensor_speed_mean_m_s": 0.009319543157955109,
  "tail_fk_speed_mean_m_s": 0.009321788424368331,
  "peak_tilt_rad": 0.04181549943421037,
  "peak_wheel_torque_nm": 0.2994846701622009,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 8.063070905045606
}
```
