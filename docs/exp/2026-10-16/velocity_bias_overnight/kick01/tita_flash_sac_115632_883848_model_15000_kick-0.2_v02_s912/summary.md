# tita_flash_sac_115632_883848_model_15000_kick-0.2_v02_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 966f7a286b3139a7c633828fa375c6eeb4645d5eed73f64ed986c1c72dc72003

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_15000_kick-0.2_v02_s912",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_15000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 912,
    "estimator": "fk",
    "runtime": true,
    "kick": -0.2,
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
  "initial_physics_sha256": "76b09a94e2e7f4c756c4fa9f802108b5b9dae82f48975ecd8f804f88a12676e6",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.03628180940093349,
  "max_drift_m": 0.0814873490786577,
  "radial_IAE_m_s": 2.219971919373132,
  "signed_longitudinal_delta_m": -0.036237233920655566,
  "tail_speed_mean_m_s": 8.634436708491856e-06,
  "tail_speed_rms_m_s": 9.369396848660666e-06,
  "tail_sensor_speed_mean_m_s": 8.906407804144275e-06,
  "tail_fk_speed_mean_m_s": 9.50138685437203e-06,
  "peak_tilt_rad": 0.16430373016949518,
  "peak_wheel_torque_nm": 4.2115397453308105,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.3397484431893735,
  "final_integral_m_s": -0.33976353737128573,
  "elapsed_wall_s": 17.625786035030615
}
```
