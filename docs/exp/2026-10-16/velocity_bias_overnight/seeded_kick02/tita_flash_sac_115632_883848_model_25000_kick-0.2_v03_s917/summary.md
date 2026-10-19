# tita_flash_sac_115632_883848_model_25000_kick-0.2_v03_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: fd99df31c9e160baa980cd421917f4536bfda16779ad79754dd3d4bf13c600b1

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_25000_kick-0.2_v03_s917",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_25000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 917,
    "estimator": "fk",
    "guarded": true,
    "kick": -0.2,
    "law": {
      "kp": 0.0,
      "ki": 4.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0,
      "seed_gain": 3.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
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
  "initial_physics_sha256": "eb5f3687019017a742c82823f57c28b9568eedb2ec54b69c358dd1adcc57147e",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.09009545946723298,
  "max_drift_m": 0.13193137570776045,
  "radial_IAE_m_s": 4.705132149504713,
  "signed_longitudinal_delta_m": 0.0900948319625789,
  "tail_speed_mean_m_s": 0.0004013745107075802,
  "tail_speed_rms_m_s": 0.00040293877975740246,
  "tail_sensor_speed_mean_m_s": 0.0004011167324502209,
  "tail_fk_speed_mean_m_s": 0.000410570990812121,
  "peak_tilt_rad": 0.13084807079648741,
  "peak_wheel_torque_nm": 1.29961097240448,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 1.3364685721783625,
  "final_integral_m_s": 1.3364685721783625,
  "elapsed_wall_s": 12.76939679600764
}
```
