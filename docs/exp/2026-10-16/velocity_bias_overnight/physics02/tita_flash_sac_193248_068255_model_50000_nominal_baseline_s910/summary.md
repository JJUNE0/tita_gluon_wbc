# tita_flash_sac_193248_068255_model_50000_nominal_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 948c108cb4740ede74b9c33fdca02f3a0bc4ae70aeb862e20f90c841243b1087

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_50000_nominal_baseline_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_50000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {},
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "948c108cb4740ede74b9c33fdca02f3a0bc4ae70aeb862e20f90c841243b1087",
  "onnx_sha256": "9edc5ad830f2e0f0d88dcb9bd8a21a023d3cdd754ce2e54339650dc66d2bb1c4",
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
  "initial_physics_sha256": "9216364b736a50a1332ac80bb7220cc6d4e34122cba3b249e5fa1041b41a894f",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 7.168892407422965,
  "max_drift_m": 7.168892407422965,
  "radial_IAE_m_s": 207.50533255787076,
  "signed_longitudinal_delta_m": 7.168010944195423,
  "tail_speed_mean_m_s": 0.12651894007078548,
  "tail_speed_rms_m_s": 0.12652322019100365,
  "tail_sensor_speed_mean_m_s": 0.12624556820723204,
  "tail_fk_speed_mean_m_s": 0.126243823381031,
  "peak_tilt_rad": 0.058448194162362466,
  "peak_wheel_torque_nm": 0.2623164653778076,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 12.776529558002949
}
```
