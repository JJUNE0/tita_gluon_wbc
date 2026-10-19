# tita_flash_sac_193248_068255_model_25000_baseline_s918_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a88ec2159129b2c9f29715b2f942b238e93417aa23bf3fefea0bf1d4336216e5

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_25000_baseline_s918_300s",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_25000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 918,
    "estimator": "fk",
    "guarded": false,
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
  },
  "checkpoint_sha256": "a88ec2159129b2c9f29715b2f942b238e93417aa23bf3fefea0bf1d4336216e5",
  "onnx_sha256": "19391bfb486479152b3d34f022849e6a9a0c6ba15be2cb35b847b19256f6e30b",
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
  "initial_physics_sha256": "80f20bafc99e0ab883576cf2e6e259a7435787c8ef1d1e59d544adb0c3939ebb",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 56.272826290172446,
  "max_drift_m": 56.272826290172446,
  "radial_IAE_m_s": 8457.923542045328,
  "signed_longitudinal_delta_m": 56.25437294207713,
  "tail_speed_mean_m_s": 0.18716469927457088,
  "tail_speed_rms_m_s": 0.18716469928815962,
  "tail_sensor_speed_mean_m_s": 0.18675945721695253,
  "tail_fk_speed_mean_m_s": 0.18675941622661268,
  "peak_tilt_rad": 0.10901722122350255,
  "peak_wheel_torque_nm": 0.10760420560836792,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 46.18118529894855
}
```
