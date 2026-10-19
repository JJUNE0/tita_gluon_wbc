# tita_flash_sac_115632_883848_model_60000_kick+0.2_v03_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_60000_kick+0.2_v03_s917",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_60000",
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
  "checkpoint_sha256": "6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05",
  "onnx_sha256": "f44f07ed44970e3ff565eae67fd9229adf0be5c02215591c52a691ffcbb71b2a",
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
  "initial_physics_sha256": "cd6a5a1b957aa9be4265fce222b445072af18c7afdd103a2696df6540b049d43",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.003956197614122705,
  "max_drift_m": 0.09443462129750226,
  "radial_IAE_m_s": 0.39796078977725846,
  "signed_longitudinal_delta_m": 0.003955093604131435,
  "tail_speed_mean_m_s": -2.4828748995741758e-05,
  "tail_speed_rms_m_s": 2.5609692398243997e-05,
  "tail_sensor_speed_mean_m_s": -2.484704515657382e-05,
  "tail_fk_speed_mean_m_s": -2.2741849214628788e-05,
  "peak_tilt_rad": 0.0964490750573892,
  "peak_wheel_torque_nm": 1.9181427955627441,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.04746885903889226,
  "final_integral_m_s": 0.04746885903889226,
  "elapsed_wall_s": 8.610000182001386
}
```
