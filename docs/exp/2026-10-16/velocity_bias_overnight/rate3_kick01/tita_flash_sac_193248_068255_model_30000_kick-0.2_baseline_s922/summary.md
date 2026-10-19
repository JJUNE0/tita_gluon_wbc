# tita_flash_sac_193248_068255_model_30000_kick-0.2_baseline_s922

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 1e8eb8c4549e7335f4ef3d31ec9b7b45fd0cb148283a41b8c616f429cefb643f

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_30000_kick-0.2_baseline_s922",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_30000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 922,
    "estimator": "fk",
    "guarded": false,
    "kick": -0.2,
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
  },
  "checkpoint_sha256": "1e8eb8c4549e7335f4ef3d31ec9b7b45fd0cb148283a41b8c616f429cefb643f",
  "onnx_sha256": "ec18f72b80fd3755cb0dce2de3434e16c4375a38100a8a08c28560539614d4a8",
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
  "initial_physics_sha256": "32f0131d36aa625568e8c5434615f220e58cb9cbe321a56c90d4d60597721046",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 2.8029849690587776,
  "max_drift_m": 2.8029849690587776,
  "radial_IAE_m_s": 80.82781708649313,
  "signed_longitudinal_delta_m": 2.802144993366714,
  "tail_speed_mean_m_s": 0.04845637062866695,
  "tail_speed_rms_m_s": 0.04845655900947463,
  "tail_sensor_speed_mean_m_s": 0.048351110005078676,
  "tail_fk_speed_mean_m_s": 0.04834986097728266,
  "peak_tilt_rad": 0.022946051104926868,
  "peak_wheel_torque_nm": 1.3373701572418213,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 7.235150567023084
}
```
