# tita_flash_sac_115632_883848_model_35000_kick+0.2_baseline_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 04d8993b85810ece43a5d202a8a86b46097dcc9e30ce2c7825e73f538f9beab6

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_35000_kick+0.2_baseline_s917",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_35000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 917,
    "estimator": "fk",
    "guarded": false,
    "kick": 0.2,
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
  },
  "checkpoint_sha256": "04d8993b85810ece43a5d202a8a86b46097dcc9e30ce2c7825e73f538f9beab6",
  "onnx_sha256": "3ce2f1cc7a17e8f712ba06efe9dc56bd55d6b0090b07942bae3238a59fef56e0",
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
  "initial_physics_sha256": "ee615353956b4b4df5e3141c9a255157782b1926bd8a92db684b5e5de47c87eb",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 13.91480028694563,
  "max_drift_m": 13.91480028694563,
  "radial_IAE_m_s": 417.5703326977723,
  "signed_longitudinal_delta_m": 13.913810295104685,
  "tail_speed_mean_m_s": 0.2324898508617943,
  "tail_speed_rms_m_s": 0.23248985337498573,
  "tail_sensor_speed_mean_m_s": 0.2319869136554858,
  "tail_fk_speed_mean_m_s": 0.23198497685965,
  "peak_tilt_rad": 0.16646872835380933,
  "peak_wheel_torque_nm": 2.611586570739746,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 13.729771156969946
}
```
