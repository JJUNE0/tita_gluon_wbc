# tita_flash_sac_115632_883848_model_70000_friction08_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 936b61280fdba31580b4cf5aba54af156eb78294655bbd493f8650181c2dd189

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_70000_friction08_baseline_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_70000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "friction": 0.8
    },
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
  "initial_physics_sha256": "18361f28d6839b7441612aa75af4744218437e26bb094215f82320b1f402b7ea",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 4.583566923205702,
  "max_drift_m": 4.583566923205702,
  "radial_IAE_m_s": 138.48989795474284,
  "signed_longitudinal_delta_m": -4.53927133535387,
  "tail_speed_mean_m_s": -0.0752353098039374,
  "tail_speed_rms_m_s": 0.0752357651214867,
  "tail_sensor_speed_mean_m_s": -0.07507514558869217,
  "tail_fk_speed_mean_m_s": -0.07507462351068901,
  "peak_tilt_rad": 0.019613504625961786,
  "peak_wheel_torque_nm": 0.11784294247627258,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.681346242025029
}
```
