# tita_flash_sac_193248_068255_model_45000_kick-0.2_v03_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 70a9e97ecbd4861ec30c17805a0e137ff6f7723b96433205dbd8c3fc0e1b103a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_45000_kick-0.2_v03_s917",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_45000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 917,
    "estimator": "fk",
    "guarded": true,
    "kick": -0.2,
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
  "checkpoint_sha256": "70a9e97ecbd4861ec30c17805a0e137ff6f7723b96433205dbd8c3fc0e1b103a",
  "onnx_sha256": "f6bd5f1e2f31278db9eb7cc34e33c35b26407a27d2b9d587a0443c3dc0ab4bb8",
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
  "initial_physics_sha256": "5811362e6da617bdbc27b6c1c48d31dbcd6d78360e177a7ce5fce0139b6d3a6e",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.00720021950438353,
  "max_drift_m": 0.1406211949489852,
  "radial_IAE_m_s": 0.7719747945934665,
  "signed_longitudinal_delta_m": -0.007195130456217614,
  "tail_speed_mean_m_s": 3.91481102018835e-05,
  "tail_speed_rms_m_s": 3.9152033504917645e-05,
  "tail_sensor_speed_mean_m_s": 3.995602502347857e-05,
  "tail_fk_speed_mean_m_s": 3.7479711734906706e-05,
  "peak_tilt_rad": 0.11864763794047417,
  "peak_wheel_torque_nm": 1.7003668546676636,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.2093846568523537,
  "final_integral_m_s": -0.2093846568523537,
  "elapsed_wall_s": 9.116461650992278
}
```
