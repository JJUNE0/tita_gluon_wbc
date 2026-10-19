# tita_flash_sac_193248_068255_model_25000_v03_s918_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a88ec2159129b2c9f29715b2f942b238e93417aa23bf3fefea0bf1d4336216e5

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_25000_v03_s918_300s",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_25000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 918,
    "estimator": "fk",
    "guarded": true,
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
  "final_drift_m": 0.05398353299590304,
  "max_drift_m": 0.07242206982221037,
  "radial_IAE_m_s": 12.825214887424181,
  "signed_longitudinal_delta_m": -0.05384071009196236,
  "tail_speed_mean_m_s": -9.864044238984275e-05,
  "tail_speed_rms_m_s": 0.00010539333830303153,
  "tail_sensor_speed_mean_m_s": -9.588480617201003e-05,
  "tail_fk_speed_mean_m_s": -9.501444449276431e-05,
  "peak_tilt_rad": 0.10852770810177015,
  "peak_wheel_torque_nm": 0.9651626348495483,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.29128784203412794,
  "final_integral_m_s": 0.29128784203412794,
  "elapsed_wall_s": 49.877786728029605
}
```
