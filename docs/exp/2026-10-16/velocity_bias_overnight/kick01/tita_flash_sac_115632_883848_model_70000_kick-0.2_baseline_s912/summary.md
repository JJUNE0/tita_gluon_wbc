# tita_flash_sac_115632_883848_model_70000_kick-0.2_baseline_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 936b61280fdba31580b4cf5aba54af156eb78294655bbd493f8650181c2dd189

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_70000_kick-0.2_baseline_s912",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_70000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 912,
    "estimator": "fk",
    "runtime": false,
    "kick": -0.2,
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "936b61280fdba31580b4cf5aba54af156eb78294655bbd493f8650181c2dd189",
  "onnx_sha256": "70370bc52ceb9baf1dff730e385c0d358159b39521a99f56af139ca34bbdccf1",
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
  "initial_physics_sha256": "7d856be8bd0ab717e7ac196bb06f510bc9e960d7b5cf3dadca39d9e300a5dbaf",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 4.701502930234543,
  "max_drift_m": 4.701502930234543,
  "radial_IAE_m_s": 146.6392867869547,
  "signed_longitudinal_delta_m": -4.685269142843698,
  "tail_speed_mean_m_s": -0.07486526098749495,
  "tail_speed_rms_m_s": 0.07486535924311385,
  "tail_sensor_speed_mean_m_s": -0.07470346151356783,
  "tail_fk_speed_mean_m_s": -0.07470317256284098,
  "peak_tilt_rad": 0.027451176764937246,
  "peak_wheel_torque_nm": 1.7801936864852905,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 12.34958334901603
}
```
