# tita_flash_sac_115632_883848_model_25000_v02_s914_900s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: fd99df31c9e160baa980cd421917f4536bfda16779ad79754dd3d4bf13c600b1

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_25000_v02_s914_900s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_25000",
    "duration": 900.0,
    "warmup": 1.2,
    "seed": 914,
    "estimator": "fk",
    "runtime": true,
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
    }
  },
  "checkpoint_sha256": "fd99df31c9e160baa980cd421917f4536bfda16779ad79754dd3d4bf13c600b1",
  "onnx_sha256": "494320c9b871a706a00e8f350ff196243c37e61c0d12ed2ab0503ea24d273b8f",
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
  "initial_physics_sha256": "4b812bd34d609053b1d507c064f920b9ae4e59441ee42ae070bdf43bd8cae15a",
  "complete": true,
  "failure": [],
  "duration_s": 900.0,
  "final_drift_m": 0.14280242910788307,
  "max_drift_m": 0.21405587588522887,
  "radial_IAE_m_s": 131.88621099602602,
  "signed_longitudinal_delta_m": 0.1371923459762738,
  "tail_speed_mean_m_s": 3.311246211218709e-06,
  "tail_speed_rms_m_s": 3.313248957989329e-06,
  "tail_sensor_speed_mean_m_s": -1.1479502467768073e-05,
  "tail_fk_speed_mean_m_s": 9.467688332330937e-10,
  "peak_tilt_rad": 0.13977401591272476,
  "peak_wheel_torque_nm": 1.462864637374878,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.963968912998138,
  "final_integral_m_s": 0.9639688375750493,
  "elapsed_wall_s": 152.71794801397482
}
```
