# tita_flash_sac_115632_883848_model_70000_baseline_s911_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 936b61280fdba31580b4cf5aba54af156eb78294655bbd493f8650181c2dd189

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_70000_baseline_s911_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_70000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 911,
    "estimator": "fk",
    "runtime": false,
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
  "initial_physics_sha256": "2a70558e7ad78ce470a1cd2a53ac3305232b0d8631393bb82eb4f45ab958315c",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 22.700683104119978,
  "max_drift_m": 22.700683104119978,
  "radial_IAE_m_s": 3386.550822668238,
  "signed_longitudinal_delta_m": -21.54910260718321,
  "tail_speed_mean_m_s": -0.08043136073059,
  "tail_speed_rms_m_s": 0.08043140372167035,
  "tail_sensor_speed_mean_m_s": -0.08030123717784775,
  "tail_fk_speed_mean_m_s": -0.08029945990468135,
  "peak_tilt_rad": 0.01938912222315259,
  "peak_wheel_torque_nm": 0.12323883175849915,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 57.441459242021665
}
```
