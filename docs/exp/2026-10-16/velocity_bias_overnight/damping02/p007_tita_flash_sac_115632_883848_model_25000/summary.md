# p007_tita_flash_sac_115632_883848_model_25000

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: fd99df31c9e160baa980cd421917f4536bfda16779ad79754dd3d4bf13c600b1

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "p007_tita_flash_sac_115632_883848_model_25000",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_25000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "analytic",
    "physics": {},
    "law": {
      "kp": 2.0,
      "ki": 15.0,
      "tau": 0.2,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0,
      "kp_fast": 3.0
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
  "initial_physics_sha256": "6a7623095d59b3790ae881c3fb20f5d23e46e39e8f7925b4c03378dac73ab1e4",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.7472989412364873,
  "max_drift_m": 0.7738789023241223,
  "radial_IAE_m_s": 31.98345844493638,
  "signed_longitudinal_delta_m": 0.7443747037849654,
  "tail_speed_mean_m_s": 0.0048798717918458745,
  "tail_speed_rms_m_s": 0.11210810146545463,
  "tail_sensor_speed_mean_m_s": 0.005086933754540111,
  "tail_fk_speed_mean_m_s": 0.0050837766384576885,
  "peak_tilt_rad": 0.1553881646213131,
  "peak_wheel_torque_nm": 1.890843391418457,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 1.0575349658920261,
  "final_integral_m_s": 1.062274670797213,
  "elapsed_wall_s": 15.003152535995468
}
```
