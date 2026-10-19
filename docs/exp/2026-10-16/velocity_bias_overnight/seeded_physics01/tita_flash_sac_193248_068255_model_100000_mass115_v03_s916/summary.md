# tita_flash_sac_193248_068255_model_100000_mass115_v03_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 2b56685ac3bb909b118178fad9d5a6eba842ceb7c9f71dc09f84de7b9d807f9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_100000_mass115_v03_s916",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_100000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "mass": 1.15
    },
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
  "checkpoint_sha256": "2b56685ac3bb909b118178fad9d5a6eba842ceb7c9f71dc09f84de7b9d807f9a",
  "onnx_sha256": "fcd7b62b26d94ec01f945f05940b24a521d0ed55477b8dfa4b0e93c3af756a6c",
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
  "initial_physics_sha256": "46d2dc46585c408eae71848e83cdc1a07cef245b10e73befb760a409d11bee8d",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.047181299879600826,
  "max_drift_m": 0.05471720073803792,
  "radial_IAE_m_s": 2.6029130928476434,
  "signed_longitudinal_delta_m": -0.04718128572355341,
  "tail_speed_mean_m_s": -0.00010904366578875051,
  "tail_speed_rms_m_s": 0.0030046235457574346,
  "tail_sensor_speed_mean_m_s": 0.0007689331237172231,
  "tail_fk_speed_mean_m_s": -3.0644955180891976e-05,
  "peak_tilt_rad": 0.08658335326393063,
  "peak_wheel_torque_nm": 2.0504164695739746,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.2666669530324475,
  "final_integral_m_s": -0.2666669530324475,
  "elapsed_wall_s": 10.392980978009291
}
```
