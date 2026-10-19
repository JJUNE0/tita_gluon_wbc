# tita_flash_sac_193248_068255_model_55000_kick+0.2_baseline_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 02d44258f752e3d43bac0b8eba0ebb2b4c1d262d812cc040b22672a16cdb583c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_55000_kick+0.2_baseline_s917",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_55000",
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
  "initial_physics_sha256": "eed1eae0af8272ec7c19e71400ef380ad6fa44e0900331ce8eeae6bc37786919",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 19.00129561441345,
  "max_drift_m": 19.00129561441345,
  "radial_IAE_m_s": 564.524566772471,
  "signed_longitudinal_delta_m": 18.768010431012524,
  "tail_speed_mean_m_s": 0.32408337762043465,
  "tail_speed_rms_m_s": 0.32408337850289654,
  "tail_sensor_speed_mean_m_s": 0.32338262726616235,
  "tail_fk_speed_mean_m_s": 0.32337591137890614,
  "peak_tilt_rad": 0.17354756661004744,
  "peak_wheel_torque_nm": 1.4528687000274658,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.807195252040401
}
```
