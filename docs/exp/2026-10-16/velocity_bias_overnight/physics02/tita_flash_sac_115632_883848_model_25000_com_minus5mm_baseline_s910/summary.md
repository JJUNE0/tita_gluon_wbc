# tita_flash_sac_115632_883848_model_25000_com_minus5mm_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: fd99df31c9e160baa980cd421917f4536bfda16779ad79754dd3d4bf13c600b1

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_25000_com_minus5mm_baseline_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_25000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
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
  "initial_physics_sha256": "13d97ef3937cbfa20edb5707e662cbd1a0753b44497b757161aacc0c1f306cbd",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 21.324012134348358,
  "max_drift_m": 21.324012134348358,
  "radial_IAE_m_s": 645.6400382972672,
  "signed_longitudinal_delta_m": 20.685448133605906,
  "tail_speed_mean_m_s": 0.3619027656016161,
  "tail_speed_rms_m_s": 0.36191867652072685,
  "tail_sensor_speed_mean_m_s": 0.3612189273891642,
  "tail_fk_speed_mean_m_s": 0.3611381370749911,
  "peak_tilt_rad": 0.13909913439573995,
  "peak_wheel_torque_nm": 0.9235541820526123,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.176309139991645
}
```
