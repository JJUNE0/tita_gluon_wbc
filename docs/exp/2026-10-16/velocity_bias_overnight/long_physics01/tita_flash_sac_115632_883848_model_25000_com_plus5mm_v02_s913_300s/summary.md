# tita_flash_sac_115632_883848_model_25000_com_plus5mm_v02_s913_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: fd99df31c9e160baa980cd421917f4536bfda16779ad79754dd3d4bf13c600b1

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_25000_com_plus5mm_v02_s913_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_25000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 913,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "com": 0.005
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
  "initial_physics_sha256": "d46689d038f20256223e4b083695967bbe2f8dc063c1f70662593dc6c6068c4c",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.16579013056353717,
  "max_drift_m": 0.22412045265946723,
  "radial_IAE_m_s": 50.913533406826645,
  "signed_longitudinal_delta_m": 0.16531332197655513,
  "tail_speed_mean_m_s": -0.00010277318543824019,
  "tail_speed_rms_m_s": 0.00010281641251079452,
  "tail_sensor_speed_mean_m_s": -0.00010973478788883085,
  "tail_fk_speed_mean_m_s": -8.988707750350626e-05,
  "peak_tilt_rad": 0.14008079116076488,
  "peak_wheel_torque_nm": 1.6950592994689941,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 1.3354024627934933,
  "final_integral_m_s": 1.3355804095739392,
  "elapsed_wall_s": 58.78758174699033
}
```
