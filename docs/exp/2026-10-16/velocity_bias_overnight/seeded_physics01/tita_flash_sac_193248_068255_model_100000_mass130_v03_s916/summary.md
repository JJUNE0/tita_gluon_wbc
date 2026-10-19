# tita_flash_sac_193248_068255_model_100000_mass130_v03_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 2b56685ac3bb909b118178fad9d5a6eba842ceb7c9f71dc09f84de7b9d807f9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_100000_mass130_v03_s916",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_100000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "mass": 1.3
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
  "initial_physics_sha256": "331d6445c8826031ef1e32a869dd94b6417e36352dd27d293dbfe5267f135980",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.032769067983130416,
  "max_drift_m": 0.06636510206454042,
  "radial_IAE_m_s": 1.5314733293998486,
  "signed_longitudinal_delta_m": -0.03276870821761632,
  "tail_speed_mean_m_s": -0.00023430719765285616,
  "tail_speed_rms_m_s": 0.009590220655497236,
  "tail_sensor_speed_mean_m_s": 0.0005870846929186901,
  "tail_fk_speed_mean_m_s": 1.2573442135262788e-05,
  "peak_tilt_rad": 0.1471220326766658,
  "peak_wheel_torque_nm": 3.5827324390411377,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.4092615914730403,
  "final_integral_m_s": -0.4092615914730403,
  "elapsed_wall_s": 10.156375953985844
}
```
