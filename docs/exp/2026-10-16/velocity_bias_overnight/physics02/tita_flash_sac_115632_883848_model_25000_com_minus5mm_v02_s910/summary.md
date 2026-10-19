# tita_flash_sac_115632_883848_model_25000_com_minus5mm_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: fd99df31c9e160baa980cd421917f4536bfda16779ad79754dd3d4bf13c600b1

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_25000_com_minus5mm_v02_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_25000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "com": -0.005
    },
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
  "initial_physics_sha256": "13d97ef3937cbfa20edb5707e662cbd1a0753b44497b757161aacc0c1f306cbd",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.13655904512437075,
  "max_drift_m": 0.2031572601900671,
  "radial_IAE_m_s": 7.920502588997658,
  "signed_longitudinal_delta_m": 0.1365548812299791,
  "tail_speed_mean_m_s": 0.00014790078641745762,
  "tail_speed_rms_m_s": 0.00014797197022922335,
  "tail_sensor_speed_mean_m_s": 0.0001481089891558762,
  "tail_fk_speed_mean_m_s": 0.00015697780826675933,
  "peak_tilt_rad": 0.13891254007651543,
  "peak_wheel_torque_nm": 1.330517053604126,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 1.2735436428454772,
  "final_integral_m_s": 1.273243197217169,
  "elapsed_wall_s": 12.436969091999345
}
```
