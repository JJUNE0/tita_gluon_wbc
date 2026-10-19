# tita_flash_sac_115632_883848_model_25000_friction02_baseline_s913_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: fd99df31c9e160baa980cd421917f4536bfda16779ad79754dd3d4bf13c600b1

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_25000_friction02_baseline_s913_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_25000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 913,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "friction": 0.2
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
  "initial_physics_sha256": "dd0628b19113a2a39ffb117c91814c99cd8fd663def9852597fa0e2dd2cf47d9",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.45351572588071126,
  "max_drift_m": 0.4537201857689799,
  "radial_IAE_m_s": 67.551897235415,
  "signed_longitudinal_delta_m": -0.44671347059462824,
  "tail_speed_mean_m_s": -0.0015345622253096667,
  "tail_speed_rms_m_s": 0.00786869340526877,
  "tail_sensor_speed_mean_m_s": 7.978177340767509,
  "tail_fk_speed_mean_m_s": 7.978156327700211,
  "peak_tilt_rad": 0.6305495487628052,
  "peak_wheel_torque_nm": 6.137844085693359,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 45.95687817200087
}
```
