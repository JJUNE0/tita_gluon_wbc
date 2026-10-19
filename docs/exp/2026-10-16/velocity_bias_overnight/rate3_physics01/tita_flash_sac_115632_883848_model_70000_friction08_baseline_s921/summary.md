# tita_flash_sac_115632_883848_model_70000_friction08_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 936b61280fdba31580b4cf5aba54af156eb78294655bbd493f8650181c2dd189

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_70000_friction08_baseline_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_70000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "friction": 0.8
    },
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
  "initial_physics_sha256": "7fcc02e6bb2ea5d74de597aec0a16cbdeb65c5b71ac8a31b025f4008041a93eb",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 4.588287777109667,
  "max_drift_m": 4.588287777109667,
  "radial_IAE_m_s": 138.67831135501552,
  "signed_longitudinal_delta_m": -4.542311644576539,
  "tail_speed_mean_m_s": -0.07526966602015582,
  "tail_speed_rms_m_s": 0.07527015365720112,
  "tail_sensor_speed_mean_m_s": -0.0751098272514557,
  "tail_fk_speed_mean_m_s": -0.07510927077185513,
  "peak_tilt_rad": 0.01963904428748231,
  "peak_wheel_torque_nm": 0.11784794926643372,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.57925285800593
}
```
