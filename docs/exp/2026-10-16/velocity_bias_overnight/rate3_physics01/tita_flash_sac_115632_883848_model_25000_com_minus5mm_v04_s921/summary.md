# tita_flash_sac_115632_883848_model_25000_com_minus5mm_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: fd99df31c9e160baa980cd421917f4536bfda16779ad79754dd3d4bf13c600b1

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_25000_com_minus5mm_v04_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_25000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "com": -0.005
    },
    "law": {
      "kp": 0.0,
      "ki": 4.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 3.0,
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
  "initial_physics_sha256": "b0a727e1b8316621ba9d73dab626801e8dd58b7e5fd666f195935fa4aace4081",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.08836175695244272,
  "max_drift_m": 0.16443124505902565,
  "radial_IAE_m_s": 4.6460455819833335,
  "signed_longitudinal_delta_m": 0.08836124899565612,
  "tail_speed_mean_m_s": 0.00038694573295685984,
  "tail_speed_rms_m_s": 0.0003872228768263869,
  "tail_sensor_speed_mean_m_s": 0.00038696165802878235,
  "tail_fk_speed_mean_m_s": 0.0003958412932344356,
  "peak_tilt_rad": 0.1387184597256339,
  "peak_wheel_torque_nm": 1.8286551237106323,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 1.2705917659703958,
  "final_integral_m_s": 1.2705917659703958,
  "elapsed_wall_s": 10.275762325967662
}
```
