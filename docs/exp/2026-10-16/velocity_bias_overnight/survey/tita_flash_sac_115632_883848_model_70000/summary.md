# tita_flash_sac_115632_883848_model_70000

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 936b61280fdba31580b4cf5aba54af156eb78294655bbd493f8650181c2dd189

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_70000",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_70000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 270,
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
  "initial_physics_sha256": "de099bf8386a2f168dbdda392ee85f1c7c770df2363a73e5c27ce6de40e92c60",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 4.530035298806794,
  "max_drift_m": 4.530035298806794,
  "radial_IAE_m_s": 136.7580754842232,
  "signed_longitudinal_delta_m": -4.518062884202761,
  "tail_speed_mean_m_s": -0.07477193320493065,
  "tail_speed_rms_m_s": 0.07477199801551399,
  "tail_sensor_speed_mean_m_s": -0.07461025758898653,
  "tail_fk_speed_mean_m_s": -0.07461000519022552,
  "peak_tilt_rad": 0.010950065086891003,
  "peak_wheel_torque_nm": 0.0681028962135315,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 4.492006321030203
}
```
