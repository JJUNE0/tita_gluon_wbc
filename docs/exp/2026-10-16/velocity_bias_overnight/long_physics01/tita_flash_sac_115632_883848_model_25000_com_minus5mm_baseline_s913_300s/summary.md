# tita_flash_sac_115632_883848_model_25000_com_minus5mm_baseline_s913_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: fd99df31c9e160baa980cd421917f4536bfda16779ad79754dd3d4bf13c600b1

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_25000_com_minus5mm_baseline_s913_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_25000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 913,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "com": -0.005
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "fd99df31c9e160baa980cd421917f4536bfda16779ad79754dd3d4bf13c600b1",
  "onnx_sha256": "494320c9b871a706a00e8f350ff196243c37e61c0d12ed2ab0503ea24d273b8f",
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
  "initial_physics_sha256": "32552f9bf60417508e0e03ef9a310be5f1885b60e90429f98c23615d156222c3",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 61.02289453737157,
  "max_drift_m": 62.07979580967544,
  "radial_IAE_m_s": 12554.227397196486,
  "signed_longitudinal_delta_m": -3.6376252110831433,
  "tail_speed_mean_m_s": 0.3619021420639056,
  "tail_speed_rms_m_s": 0.36191805402669264,
  "tail_sensor_speed_mean_m_s": 0.36121814469534747,
  "tail_fk_speed_mean_m_s": 0.3611375218828594,
  "peak_tilt_rad": 0.13879395167006248,
  "peak_wheel_torque_nm": 0.9162518978118896,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 42.22264881298179
}
```
