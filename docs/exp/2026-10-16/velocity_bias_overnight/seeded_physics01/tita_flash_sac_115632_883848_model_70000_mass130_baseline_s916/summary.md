# tita_flash_sac_115632_883848_model_70000_mass130_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 936b61280fdba31580b4cf5aba54af156eb78294655bbd493f8650181c2dd189

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_70000_mass130_baseline_s916",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_70000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "mass": 1.3
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
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
  "initial_physics_sha256": "1861cacd271b6841a764edcc5403fdd037b2b340860fdee2f9e920c1b0b776c8",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 9.783781083954773,
  "max_drift_m": 9.783781083954773,
  "radial_IAE_m_s": 293.94755797396226,
  "signed_longitudinal_delta_m": -9.782629786819024,
  "tail_speed_mean_m_s": -0.162480259084659,
  "tail_speed_rms_m_s": 0.16248042548849734,
  "tail_sensor_speed_mean_m_s": -0.1621313310872351,
  "tail_fk_speed_mean_m_s": -0.16213096448318792,
  "peak_tilt_rad": 0.022684160441677967,
  "peak_wheel_torque_nm": 0.27498894929885864,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 10.523575085040648
}
```
