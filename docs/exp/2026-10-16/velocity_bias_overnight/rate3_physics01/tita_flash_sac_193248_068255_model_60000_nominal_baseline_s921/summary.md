# tita_flash_sac_193248_068255_model_60000_nominal_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 9b0d8897472dc567619d49df3e6df08813dcbb15b018f23ed58060e92e1b139b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_60000_nominal_baseline_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_60000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": false,
    "physics": {},
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
  },
  "checkpoint_sha256": "9b0d8897472dc567619d49df3e6df08813dcbb15b018f23ed58060e92e1b139b",
  "onnx_sha256": "bd80a0d28ffd69209d8e2ef2f6d867ca3f72a00abd0a3c8dbb0b6def13e19b7e",
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
  "initial_physics_sha256": "9f16babf4646c54c00492516ac58da67ebcd65931789bb3a4f167f8fb6781441",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.34642530687699563,
  "max_drift_m": 0.34642530687699563,
  "radial_IAE_m_s": 12.12401253748231,
  "signed_longitudinal_delta_m": -0.3461640628500313,
  "tail_speed_mean_m_s": -0.0038916768641274885,
  "tail_speed_rms_m_s": 0.003925345143347115,
  "tail_sensor_speed_mean_m_s": -0.0038831480996413294,
  "tail_fk_speed_mean_m_s": -0.003881059723291116,
  "peak_tilt_rad": 0.034084577916967174,
  "peak_wheel_torque_nm": 0.09894503653049469,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 7.62229498999659
}
```
