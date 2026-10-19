# tita_flash_sac_115632_883848_model_65000_kick+0.2_v03_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a28e8551929d9a4412f571a2e91577da75879477c15d61f0774ab6f05354dff3

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_65000_kick+0.2_v03_s917",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_65000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 917,
    "estimator": "fk",
    "guarded": true,
    "kick": 0.2,
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
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
  },
  "checkpoint_sha256": "a28e8551929d9a4412f571a2e91577da75879477c15d61f0774ab6f05354dff3",
  "onnx_sha256": "7cc289e8aee44513f1e29487c7522e96c762174e2444aedaa7aea78b3a66a3ec",
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
  "initial_physics_sha256": "f4d6c3ddede1dbe3112f9c969a3a10a45b61d9a35fa847ea3835f103cb15bf97",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.0007459406867555106,
  "max_drift_m": 0.10819955683833972,
  "radial_IAE_m_s": 0.2827960147906077,
  "signed_longitudinal_delta_m": -8.205098350655552e-05,
  "tail_speed_mean_m_s": -2.4278301266463328e-05,
  "tail_speed_rms_m_s": 2.430542119795491e-05,
  "tail_sensor_speed_mean_m_s": -2.4022422899748692e-05,
  "tail_fk_speed_mean_m_s": -2.5209968831629413e-05,
  "peak_tilt_rad": 0.08078376916730678,
  "peak_wheel_torque_nm": 1.5636460781097412,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.04949054743171307,
  "final_integral_m_s": 0.04949054743171307,
  "elapsed_wall_s": 8.994783788977657
}
```
