# tita_flash_sac_115632_883848_model_45000_mass130_b+0.030

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 43062a7c7858bfeb0cce0542eb1f4a18dfcde51a093f58d89c7806ec35643067

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_45000_mass130_b+0.030",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_45000",
    "duration": 120.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "physics": {
      "mass": 1.3
    },
    "law": {
      "mode": "constant",
      "bias": 0.03,
      "limit": 2.0,
      "slew": 2.0,
      "ramp": 0.25
    }
  },
  "checkpoint_sha256": "43062a7c7858bfeb0cce0542eb1f4a18dfcde51a093f58d89c7806ec35643067",
  "onnx_sha256": "7b25c8c9afe56cdbfe483aa15167008f11b20e96722bf811b19fa3d80bf0e8e5",
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
  "initial_physics_sha256": "3a4ba1ca68189c8896b3491841cd28abf61e8aa5305f036f14ac64ec8a9f372d",
  "complete": true,
  "failure": [],
  "duration_s": 120.0,
  "final_drift_m": 20.171843374768553,
  "max_drift_m": 21.177831148013244,
  "radial_IAE_m_s": 1473.6607946005267,
  "signed_longitudinal_delta_m": -16.99942624886323,
  "tail_speed_mean_m_s": -0.22311717971135833,
  "tail_speed_rms_m_s": 0.2231837086516957,
  "tail_sensor_speed_mean_m_s": -0.22262846035752523,
  "tail_fk_speed_mean_m_s": -0.22286034558079393,
  "peak_tilt_rad": 0.035053922279826066,
  "peak_wheel_torque_nm": 0.6980220079421997,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.03,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 26.230090490018483
}
```
