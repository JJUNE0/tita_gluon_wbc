# tita_flash_sac_115632_883848_model_70000_kick+0.2_baseline_s922

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 936b61280fdba31580b4cf5aba54af156eb78294655bbd493f8650181c2dd189

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_70000_kick+0.2_baseline_s922",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_70000",
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
  "checkpoint_sha256": "936b61280fdba31580b4cf5aba54af156eb78294655bbd493f8650181c2dd189",
  "onnx_sha256": "70370bc52ceb9baf1dff730e385c0d358159b39521a99f56af139ca34bbdccf1",
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
  "initial_physics_sha256": "8bfb99ba28aaa94d44d8b49ab8e48f153810e18de6c01b14db4756faeb996396",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 4.325956662087783,
  "max_drift_m": 4.325956662087783,
  "radial_IAE_m_s": 124.56102014660212,
  "signed_longitudinal_delta_m": -4.311182937306606,
  "tail_speed_mean_m_s": -0.0749058398421957,
  "tail_speed_rms_m_s": 0.07490596251656037,
  "tail_sensor_speed_mean_m_s": -0.0747439174506434,
  "tail_fk_speed_mean_m_s": -0.0747436739992143,
  "peak_tilt_rad": 0.04770728807006108,
  "peak_wheel_torque_nm": 1.4990315437316895,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.054167815949768
}
```
