# tita_flash_sac_193248_068255_model_90000_kick+0.2_baseline_s922

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d94ec425dcab69bfb8001711468b6ca37297f4e1aec2e9b20535fd106ee98769

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_90000_kick+0.2_baseline_s922",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_90000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 922,
    "estimator": "fk",
    "guarded": false,
    "kick": 0.2,
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
  },
  "checkpoint_sha256": "d94ec425dcab69bfb8001711468b6ca37297f4e1aec2e9b20535fd106ee98769",
  "onnx_sha256": "aff309a07b913000eb7916a9b3867232296f7834f48d5391c16e7ec4e09b84d2",
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
  "initial_physics_sha256": "d73a227ede720db9a5ab99f64fc8cada00b5d39dd00c0e8540962aae910117d0",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 13.342482642855396,
  "max_drift_m": 13.342482642855396,
  "radial_IAE_m_s": 400.60262266740796,
  "signed_longitudinal_delta_m": 13.334662644633836,
  "tail_speed_mean_m_s": 0.22359428783465551,
  "tail_speed_rms_m_s": 0.2235943729734796,
  "tail_sensor_speed_mean_m_s": 0.22311062888662203,
  "tail_fk_speed_mean_m_s": 0.22310829276258803,
  "peak_tilt_rad": 0.11432830810490935,
  "peak_wheel_torque_nm": 1.22934091091156,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 16.25772935996065
}
```
