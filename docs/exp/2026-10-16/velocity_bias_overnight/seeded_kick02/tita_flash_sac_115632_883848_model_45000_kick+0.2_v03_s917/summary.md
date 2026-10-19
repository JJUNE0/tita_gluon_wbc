# tita_flash_sac_115632_883848_model_45000_kick+0.2_v03_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 43062a7c7858bfeb0cce0542eb1f4a18dfcde51a093f58d89c7806ec35643067

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_45000_kick+0.2_v03_s917",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_45000",
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
  "checkpoint_sha256": "43062a7c7858bfeb0cce0542eb1f4a18dfcde51a093f58d89c7806ec35643067",
  "onnx_sha256": "7b25c8c9afe56cdbfe483aa15167008f11b20e96722bf811b19fa3d80bf0e8e5",
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
  "initial_physics_sha256": "ea4263088e8f522b8eb4c34f320c53f11803e6e22c7eb9d3a5e425277f8c6c69",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.004329006972477207,
  "max_drift_m": 0.0811309938406568,
  "radial_IAE_m_s": 0.4756121341851707,
  "signed_longitudinal_delta_m": 0.003076052454833246,
  "tail_speed_mean_m_s": -0.00013656443967898497,
  "tail_speed_rms_m_s": 0.007487241712303771,
  "tail_sensor_speed_mean_m_s": -0.0005209332465567296,
  "tail_fk_speed_mean_m_s": 8.893103535246302e-05,
  "peak_tilt_rad": 0.06220812641377882,
  "peak_wheel_torque_nm": 4.9845428466796875,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.14922565584678948,
  "final_integral_m_s": 0.14922565584678948,
  "elapsed_wall_s": 14.371006508998107
}
```
