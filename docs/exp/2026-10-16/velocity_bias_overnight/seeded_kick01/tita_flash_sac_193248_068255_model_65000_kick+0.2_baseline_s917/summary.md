# tita_flash_sac_193248_068255_model_65000_kick+0.2_baseline_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 950b5958dfae8344a2f3cfbf5d26f83d6cac60eaaf404962bb8ea0b163f7244e

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_65000_kick+0.2_baseline_s917",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_65000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 917,
    "estimator": "fk",
    "guarded": false,
    "kick": 0.2,
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
  },
  "checkpoint_sha256": "950b5958dfae8344a2f3cfbf5d26f83d6cac60eaaf404962bb8ea0b163f7244e",
  "onnx_sha256": "a1f326d5979e91ea8e5b962f09eb3e8da4d889ac9902563756ff9179048872c8",
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
  "initial_physics_sha256": "d2d4bd41d4293231ab9b42dcb53a2baa368db90eaa3252b0fe57464d9a38f2a5",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 2.3987401624391054,
  "max_drift_m": 2.3987401624391054,
  "radial_IAE_m_s": 66.84483310850086,
  "signed_longitudinal_delta_m": -2.3949875029581027,
  "tail_speed_mean_m_s": -0.04294390061724503,
  "tail_speed_rms_m_s": 0.04294433456245039,
  "tail_sensor_speed_mean_m_s": -0.04285768152237892,
  "tail_fk_speed_mean_m_s": -0.0428525217598196,
  "peak_tilt_rad": 0.057085092850577945,
  "peak_wheel_torque_nm": 1.749706745147705,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 12.099745620042086
}
```
