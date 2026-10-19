# tita_flash_sac_115632_883848_model_15000_friction02_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 966f7a286b3139a7c633828fa375c6eeb4645d5eed73f64ed986c1c72dc72003

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_15000_friction02_baseline_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_15000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
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
  "initial_physics_sha256": "3f53b2d0007038b1e0695650335791e87afb18abbb86bbe70057a3a9ba4af368",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 6.458699305651997,
  "max_drift_m": 6.458699305651997,
  "radial_IAE_m_s": 199.59927015688947,
  "signed_longitudinal_delta_m": -6.3490040479802055,
  "tail_speed_mean_m_s": -0.1015800576511229,
  "tail_speed_rms_m_s": 0.10159086641286756,
  "tail_sensor_speed_mean_m_s": -0.10142337602430478,
  "tail_fk_speed_mean_m_s": -0.10141841343656571,
  "peak_tilt_rad": 0.06375007477304684,
  "peak_wheel_torque_nm": 1.861629843711853,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 17.375416106020566
}
```
