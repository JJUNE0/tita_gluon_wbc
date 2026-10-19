# tita_flash_sac_193248_068255_model_55000_kick-0.2_baseline_s922

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 02d44258f752e3d43bac0b8eba0ebb2b4c1d262d812cc040b22672a16cdb583c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_55000_kick-0.2_baseline_s922",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_55000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 922,
    "estimator": "fk",
    "guarded": false,
    "kick": -0.2,
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
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
  "initial_physics_sha256": "02f36a2a0a95dc1ca4be7c239719181044f2d86010d5ac14ddd2cabaf1c01bb6",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 17.983318743345556,
  "max_drift_m": 17.983318743345556,
  "radial_IAE_m_s": 506.1794332590267,
  "signed_longitudinal_delta_m": 17.756786420028384,
  "tail_speed_mean_m_s": 0.324064857376088,
  "tail_speed_rms_m_s": 0.3240648598020573,
  "tail_sensor_speed_mean_m_s": 0.3233641682510975,
  "tail_fk_speed_mean_m_s": 0.3233574299647574,
  "peak_tilt_rad": 0.17354712124386995,
  "peak_wheel_torque_nm": 1.4762990474700928,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 8.162725863978267
}
```
