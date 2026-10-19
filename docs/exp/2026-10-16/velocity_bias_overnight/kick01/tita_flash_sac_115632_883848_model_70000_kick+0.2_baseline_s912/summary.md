# tita_flash_sac_115632_883848_model_70000_kick+0.2_baseline_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 936b61280fdba31580b4cf5aba54af156eb78294655bbd493f8650181c2dd189

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_70000_kick+0.2_baseline_s912",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_70000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 912,
    "estimator": "fk",
    "runtime": false,
    "kick": 0.2,
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
  "initial_physics_sha256": "57a64db9bd594ad470136146efcfa9d946c1b74fc3cfa8cb08284272c702ba34",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 4.3259560862513435,
  "max_drift_m": 4.3259560862513435,
  "radial_IAE_m_s": 124.56098124095023,
  "signed_longitudinal_delta_m": -4.311182435024235,
  "tail_speed_mean_m_s": -0.07490585365351478,
  "tail_speed_rms_m_s": 0.07490597635239649,
  "tail_sensor_speed_mean_m_s": -0.07474393246512888,
  "tail_fk_speed_mean_m_s": -0.07474368777319668,
  "peak_tilt_rad": 0.047707290050673645,
  "peak_wheel_torque_nm": 1.4990419149398804,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 10.616392954951152
}
```
