# tita_flash_sac_193248_068255_model_65000_kick-0.2_baseline_s922

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 950b5958dfae8344a2f3cfbf5d26f83d6cac60eaaf404962bb8ea0b163f7244e

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_65000_kick-0.2_baseline_s922",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_65000",
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
  "initial_physics_sha256": "2ff281d10b1e5948440232a8c82aae6a1f1b7af4801c06bb993acca22aefcab5",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 2.828789280631616,
  "max_drift_m": 2.828789280631616,
  "radial_IAE_m_s": 91.56751077055922,
  "signed_longitudinal_delta_m": -2.825978090100714,
  "tail_speed_mean_m_s": -0.04292440178833101,
  "tail_speed_rms_m_s": 0.0429248380333708,
  "tail_sensor_speed_mean_m_s": -0.042838121821618384,
  "tail_fk_speed_mean_m_s": -0.042832957631878915,
  "peak_tilt_rad": 0.02944055060453521,
  "peak_wheel_torque_nm": 1.7681381702423096,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 7.198442812019493
}
```
