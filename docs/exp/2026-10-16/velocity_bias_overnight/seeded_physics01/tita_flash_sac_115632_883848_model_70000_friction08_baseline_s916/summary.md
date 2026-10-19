# tita_flash_sac_115632_883848_model_70000_friction08_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 936b61280fdba31580b4cf5aba54af156eb78294655bbd493f8650181c2dd189

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_70000_friction08_baseline_s916",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_70000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "friction": 0.8
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
  "initial_physics_sha256": "ad05eb8966dc271b530e86fc86931ded436fd288359998ad00d0161f7086e402",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 4.58828822082068,
  "max_drift_m": 4.58828822082068,
  "radial_IAE_m_s": 138.67833994111297,
  "signed_longitudinal_delta_m": -4.5423120821374825,
  "tail_speed_mean_m_s": -0.0752696556597581,
  "tail_speed_rms_m_s": 0.07527014331314177,
  "tail_sensor_speed_mean_m_s": -0.0751098166001356,
  "tail_fk_speed_mean_m_s": -0.07510926059118384,
  "peak_tilt_rad": 0.019639060220613125,
  "peak_wheel_torque_nm": 0.11784327030181885,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 10.06309875001898
}
```
