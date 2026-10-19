# tita_flash_sac_115632_883848_model_15000_mass130_analytic

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 966f7a286b3139a7c633828fa375c6eeb4645d5eed73f64ed986c1c72dc72003

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_15000_mass130_analytic",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_15000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 272,
    "estimator": "analytic",
    "physics": {
      "mass": 1.3
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
  "checkpoint_sha256": "966f7a286b3139a7c633828fa375c6eeb4645d5eed73f64ed986c1c72dc72003",
  "onnx_sha256": "1fec00b7bc7eebbc5b6decf23ac6f29b8799c5cf64ff1dee51c1ba762cf013ed",
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
  "initial_physics_sha256": "ca22b1799858dc54b831f559c46d00ba9d88842bf263ac9dacc4b3975fa7e33d",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.017167481159609862,
  "max_drift_m": 0.03127726785110291,
  "radial_IAE_m_s": 0.8402406271036095,
  "signed_longitudinal_delta_m": 0.015680239868186417,
  "tail_speed_mean_m_s": 0.0006688270153240277,
  "tail_speed_rms_m_s": 0.02697497501826447,
  "tail_sensor_speed_mean_m_s": 0.0007935372498444187,
  "tail_fk_speed_mean_m_s": -5.418540795190896e-05,
  "peak_tilt_rad": 0.18477961149683986,
  "peak_wheel_torque_nm": 7.089982986450195,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.30146559806452106,
  "final_integral_m_s": -0.33247524941229284,
  "elapsed_wall_s": 14.916154350969009
}
```
