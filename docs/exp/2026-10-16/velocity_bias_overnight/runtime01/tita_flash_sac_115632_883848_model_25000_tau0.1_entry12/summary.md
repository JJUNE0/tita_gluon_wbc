# tita_flash_sac_115632_883848_model_25000_tau0.1_entry12

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: fd99df31c9e160baa980cd421917f4536bfda16779ad79754dd3d4bf13c600b1

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_25000_tau0.1_entry12",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_25000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 271,
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
  "initial_physics_sha256": "17c8e89bcd920956da58340cfe7614ce3f0d7d132db8607265b0c5ba81c2a0b4",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.15401370325325708,
  "max_drift_m": 0.21399334663055886,
  "radial_IAE_m_s": 8.964749228809566,
  "signed_longitudinal_delta_m": 0.1540078588268135,
  "tail_speed_mean_m_s": 0.0001434023827631537,
  "tail_speed_rms_m_s": 0.0001453696427946847,
  "tail_sensor_speed_mean_m_s": 0.00014284010552126927,
  "tail_fk_speed_mean_m_s": 0.00015225821903572768,
  "peak_tilt_rad": 0.1397165286887163,
  "peak_wheel_torque_nm": 1.4569079875946045,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 1.341236902324209,
  "final_integral_m_s": 1.3410138096235185,
  "elapsed_wall_s": 6.184726947976742
}
```
