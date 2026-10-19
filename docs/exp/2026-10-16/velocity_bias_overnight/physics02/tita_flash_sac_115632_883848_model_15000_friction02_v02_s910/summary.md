# tita_flash_sac_115632_883848_model_15000_friction02_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 966f7a286b3139a7c633828fa375c6eeb4645d5eed73f64ed986c1c72dc72003

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_15000_friction02_v02_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_15000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "friction": 0.2
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
  "initial_physics_sha256": "3f53b2d0007038b1e0695650335791e87afb18abbb86bbe70057a3a9ba4af368",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.032830289822668335,
  "max_drift_m": 0.03935813302476034,
  "radial_IAE_m_s": 1.9713086519618022,
  "signed_longitudinal_delta_m": -0.03277891733560824,
  "tail_speed_mean_m_s": 2.8982046382501133e-06,
  "tail_speed_rms_m_s": 2.9005603941948666e-06,
  "tail_sensor_speed_mean_m_s": 3.0579587088318566e-06,
  "tail_fk_speed_mean_m_s": 3.2868411201343107e-06,
  "peak_tilt_rad": 0.12353056945235585,
  "peak_wheel_torque_nm": 2.583373546600342,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.3547797530619001,
  "final_integral_m_s": -0.3547859456571994,
  "elapsed_wall_s": 18.136569474008866
}
```
