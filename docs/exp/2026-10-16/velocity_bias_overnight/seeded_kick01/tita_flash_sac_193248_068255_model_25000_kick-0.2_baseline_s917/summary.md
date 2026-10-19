# tita_flash_sac_193248_068255_model_25000_kick-0.2_baseline_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a88ec2159129b2c9f29715b2f942b238e93417aa23bf3fefea0bf1d4336216e5

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_25000_kick-0.2_baseline_s917",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_25000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 917,
    "estimator": "fk",
    "guarded": false,
    "kick": -0.2,
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
  "initial_physics_sha256": "7de2925dd020b5186a5f4b2c69680a281a76d40e7533eded50d7945220dd660f",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 11.228484457155476,
  "max_drift_m": 11.228484457155476,
  "radial_IAE_m_s": 334.622686524347,
  "signed_longitudinal_delta_m": 11.218856935237918,
  "tail_speed_mean_m_s": 0.18767047800452127,
  "tail_speed_rms_m_s": 0.18767056819035582,
  "tail_sensor_speed_mean_m_s": 0.18726421608224367,
  "tail_fk_speed_mean_m_s": 0.18726406157067385,
  "peak_tilt_rad": 0.1095306352282579,
  "peak_wheel_torque_nm": 1.5236021280288696,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.067932114005089
}
```
