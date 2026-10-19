# tita_flash_sac_193248_068255_model_55000_kick-0.2_baseline_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 02d44258f752e3d43bac0b8eba0ebb2b4c1d262d812cc040b22672a16cdb583c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_55000_kick-0.2_baseline_s917",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_55000",
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
  "checkpoint_sha256": "02d44258f752e3d43bac0b8eba0ebb2b4c1d262d812cc040b22672a16cdb583c",
  "onnx_sha256": "98bc9d9fb343d683cc0b87892391ac7fee7f391381ceff241490864772abca13",
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
  "initial_physics_sha256": "138467cf451814c60aab717f290ee3ec919dfd1e7247d77652ed364a0a2c41a7",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 17.966172317251004,
  "max_drift_m": 17.966172317251004,
  "radial_IAE_m_s": 505.26945067692407,
  "signed_longitudinal_delta_m": 17.745126779316966,
  "tail_speed_mean_m_s": 0.3240635153522472,
  "tail_speed_rms_m_s": 0.32406351792099314,
  "tail_sensor_speed_mean_m_s": 0.32336283110783126,
  "tail_fk_speed_mean_m_s": 0.32335609111643726,
  "peak_tilt_rad": 0.17354708715014966,
  "peak_wheel_torque_nm": 1.478668212890625,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.079363122000359
}
```
