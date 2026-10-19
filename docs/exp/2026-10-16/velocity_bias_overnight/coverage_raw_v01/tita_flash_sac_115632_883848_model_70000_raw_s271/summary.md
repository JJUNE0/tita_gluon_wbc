# tita_flash_sac_115632_883848_model_70000_raw_s271

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 936b61280fdba31580b4cf5aba54af156eb78294655bbd493f8650181c2dd189

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_70000_raw_s271",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_70000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 271,
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.05,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
    },
    "estimator": "raw"
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
  "initial_physics_sha256": "3e5bfa80ada2389eb6504b64d974f16a0c6bf6a45f4fc2144905665d76815f0f",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.014553080801723638,
  "max_drift_m": 0.026501878120150688,
  "radial_IAE_m_s": 0.796578176293746,
  "signed_longitudinal_delta_m": -0.014487417181261987,
  "tail_speed_mean_m_s": -4.4661450245258475e-06,
  "tail_speed_rms_m_s": 0.009228396305970424,
  "tail_sensor_speed_mean_m_s": 0.00043589808486183364,
  "tail_fk_speed_mean_m_s": 4.04016827668259e-05,
  "peak_tilt_rad": 0.06277998471505253,
  "peak_wheel_torque_nm": 1.3774516582489014,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.024039135275484243,
  "final_integral_m_s": -0.13913332065207193,
  "elapsed_wall_s": 4.443563298031222
}
```
