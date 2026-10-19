# tita_flash_sac_115632_883848_model_70000_tau0.05_entry12

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 936b61280fdba31580b4cf5aba54af156eb78294655bbd493f8650181c2dd189

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_70000_tau0.05_entry12",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_70000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 271,
    "estimator": "fk",
    "runtime": true,
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.05,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
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
  "initial_physics_sha256": "601f58acccaa0d4eb3c819b68e4bdee915e6ac077350e2d5141aca0af453e66a",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.011882491612134907,
  "max_drift_m": 0.02010208462462921,
  "radial_IAE_m_s": 0.7206429642173354,
  "signed_longitudinal_delta_m": -0.011855971291173445,
  "tail_speed_mean_m_s": 2.4937601183708942e-06,
  "tail_speed_rms_m_s": 3.067777468255234e-06,
  "tail_sensor_speed_mean_m_s": 2.455934889626143e-06,
  "tail_fk_speed_mean_m_s": 2.505670205463966e-06,
  "peak_tilt_rad": 0.04004796823537071,
  "peak_wheel_torque_nm": 0.4092848002910614,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.12259588997684662,
  "final_integral_m_s": -0.12259540037158877,
  "elapsed_wall_s": 5.90037162398221
}
```
