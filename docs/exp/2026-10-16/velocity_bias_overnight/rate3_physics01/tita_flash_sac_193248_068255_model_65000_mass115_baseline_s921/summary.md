# tita_flash_sac_193248_068255_model_65000_mass115_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 950b5958dfae8344a2f3cfbf5d26f83d6cac60eaaf404962bb8ea0b163f7244e

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_65000_mass115_baseline_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_65000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "mass": 1.15
    },
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
  "initial_physics_sha256": "276cbace27a761dbf3349ebaeabc7f19c6720fa31846172977ac3ee59efadf58",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 7.709369842204039,
  "max_drift_m": 7.709369842204039,
  "radial_IAE_m_s": 231.0279401113412,
  "signed_longitudinal_delta_m": -7.696542975770926,
  "tail_speed_mean_m_s": -0.1287437112225551,
  "tail_speed_rms_m_s": 0.1287437113020263,
  "tail_sensor_speed_mean_m_s": -0.12850819101304173,
  "tail_fk_speed_mean_m_s": -0.1285047033194847,
  "peak_tilt_rad": 0.026575174972815585,
  "peak_wheel_torque_nm": 0.09672456979751587,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.768061103997752
}
```
