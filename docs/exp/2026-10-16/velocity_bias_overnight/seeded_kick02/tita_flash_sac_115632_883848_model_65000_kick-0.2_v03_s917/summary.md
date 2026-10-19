# tita_flash_sac_115632_883848_model_65000_kick-0.2_v03_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a28e8551929d9a4412f571a2e91577da75879477c15d61f0774ab6f05354dff3

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_65000_kick-0.2_v03_s917",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_65000",
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
  "initial_physics_sha256": "8a7543f4a5c8ceb60651fb07f7f9a753a67a22b34956a7d1184b0175550cf2c3",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.002824723987393075,
  "max_drift_m": 0.0801242795508285,
  "radial_IAE_m_s": 0.2837651701090956,
  "signed_longitudinal_delta_m": -0.0027343828518460555,
  "tail_speed_mean_m_s": -2.4813923691365465e-05,
  "tail_speed_rms_m_s": 2.4840844182681854e-05,
  "tail_sensor_speed_mean_m_s": -2.4540524410827458e-05,
  "tail_fk_speed_mean_m_s": -2.5723804220267998e-05,
  "peak_tilt_rad": 0.08258032280764627,
  "peak_wheel_torque_nm": 1.5129859447479248,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.049743775884073985,
  "final_integral_m_s": 0.049743775884073985,
  "elapsed_wall_s": 9.482137603976298
}
```
