# tita_flash_sac_115632_883848_model_70000_com_minus5mm_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 936b61280fdba31580b4cf5aba54af156eb78294655bbd493f8650181c2dd189

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_70000_com_minus5mm_baseline_s916",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_70000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "com": -0.005
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
  "initial_physics_sha256": "0d55cb462475e2975d3c6661063f9e677ee4425f73f69acd3ae4bb132d92bc52",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 5.663341206333179,
  "max_drift_m": 5.663341206333179,
  "radial_IAE_m_s": 170.1252191667619,
  "signed_longitudinal_delta_m": -5.618579194278443,
  "tail_speed_mean_m_s": -0.09408666933543304,
  "tail_speed_rms_m_s": 0.0940867015439683,
  "tail_sensor_speed_mean_m_s": -0.0938829349539876,
  "tail_fk_speed_mean_m_s": -0.09388215958322893,
  "peak_tilt_rad": 0.017340020546963375,
  "peak_wheel_torque_nm": 0.11697894334793091,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 10.043614671041723
}
```
