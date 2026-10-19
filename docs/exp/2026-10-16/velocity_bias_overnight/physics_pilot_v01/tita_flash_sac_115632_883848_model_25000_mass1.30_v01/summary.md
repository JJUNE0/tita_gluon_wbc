# tita_flash_sac_115632_883848_model_25000_mass1.30_v01

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: fd99df31c9e160baa980cd421917f4536bfda16779ad79754dd3d4bf13c600b1

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_25000_mass1.30_v01",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_25000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 272,
    "physics": {
      "mass": 1.3
    },
    "kick": 0.0,
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.05,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
    },
    "estimator": "fk"
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
  "initial_physics_sha256": "f2abcc0ff3c285cec9bdaca65a03d7f4844531bf6f4e8f1a3cf42f588b88824d",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.016896254422884744,
  "max_drift_m": 0.03180424539554804,
  "radial_IAE_m_s": 1.0181750163616656,
  "signed_longitudinal_delta_m": 0.01687150308303466,
  "tail_speed_mean_m_s": -5.876302123426008e-07,
  "tail_speed_rms_m_s": 1.2657649929894625e-06,
  "tail_sensor_speed_mean_m_s": -6.44748150080657e-07,
  "tail_fk_speed_mean_m_s": 2.7386607226742915e-09,
  "peak_tilt_rad": 0.11172707997993991,
  "peak_wheel_torque_nm": 1.5338923931121826,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.18127672018201568,
  "final_integral_m_s": 0.1812797715970442,
  "elapsed_wall_s": 5.458674686960876
}
```
